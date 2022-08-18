from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from sqlalchemy import func
import hashlib


from app import app, db
from app.forms import LoginForm, RegistrationForm, UploadForm, CourseResourcesForm
from app.models import ResourceToCourse, ResourceToUser, User, Subject, Resource, Course
import pandas as pd
import json


@app.route('/')
def index():
    courses = Course.query.all()
    return render_template("index.html", title='Home Page', courses=courses)


@app.route('/upload/<course_id>', methods=['GET', 'POST'])
def upload(course_id):
    all_subjects = Subject.query.all()
    all_subject_names = [subject.name for subject in all_subjects]
    if (all_subject_names is not None):
        all_subject_names.sort()

    form = UploadForm()
    form.subject.choices = all_subject_names

    if form.validate_on_submit():
        if not form.header.data:
            form.header.data = "ללא כותרת"

        resource = Resource(link=form.link.data,
                            solution=form.solution.data,
                            recording=form.recording.data,
                            subject=json.dumps(form.subject.data),
                            textdump=form.textdump.data.lower())
        db.session.add(resource)

        db.session.commit()
        db.session.refresh(resource)

        same_tab_count = ResourceToCourse.query.filter_by(
            course_id=course_id, tab=form.tab.data).count()

        same_tab_and_header_max = db.session.query(func.max(ResourceToCourse.order_in_tab)).filter_by(
            course_id=course_id, tab=form.tab.data, header=form.header.data).scalar()
        if not same_tab_and_header_max:
            same_tab_and_header_max = 0

        new_resource_order_in_tab = same_tab_and_header_max+1
        if new_resource_order_in_tab == 1:
            new_resource_order_in_tab = same_tab_count + 1

        if not form.rname_part.data:
            form.rname_part.data = None
        # Adjust order of existing entries
        ResourceToCourse.query.filter(
            ResourceToCourse.order_in_tab >= new_resource_order_in_tab).filter_by(
            course_id=course_id, tab=form.tab.data).update({'order_in_tab': ResourceToCourse.order_in_tab + 1})

        resource_to_course = ResourceToCourse(
            course_id=course_id, resource_id=resource.id, header=form.header.data, rname=form.rname.data, rname_part=form.rname_part.data, tab=form.tab.data, order_in_tab=new_resource_order_in_tab)
        db.session.add(resource_to_course)

        db.session.commit()

        return redirect(url_for('course', course_id=course_id))

    return render_template('upload.html', title='upload', form=form, options=all_subject_names, with_name=True)


@app.route('/edit/<resource_id>', methods=['GET', 'POST'])
def edit(resource_id):
    all_subjects = Subject.query.all()
    all_subject_names = [subject.name for subject in all_subjects]
    if (all_subject_names is not None):
        all_subject_names.sort()

    form = UploadForm()
    form.subject.choices = all_subject_names

    resource = Resource.query.filter_by(id=resource_id).first()

    if form.validate_on_submit():
        resource.link = form.link.data
        resource.solution = form.solution.data
        resource.recording = form.recording.data
        resource.subject = json.dumps(form.subject.data)
        resource.textdump = form.textdump.data.lower()
        db.session.commit()
        db.session.refresh(resource)
        return redirect(url_for('course', course_id=request.args.get('course_id')))

    else:
        print("hi")
        form.link.data = resource.link
        form.solution.data = resource.solution
        form.recording.data = resource.recording
        form.subject.data = json.loads(resource.subject)
        form.textdump.data = resource.textdump

    return render_template('upload.html', title='upload', form=form, options=all_subject_names, with_name=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('שם המשתמש או הסיסמה שגויים')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(),
                    email=form.email.data.lower(),
                    is_admin=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', title='register', form=form)


@app.route('/exams/<course_id>', methods=['GET', 'POST'])
def exams(course_id):
    return _course(course_id, "exams")


@app.route('/archive/<course_id>', methods=['GET', 'POST'])
def archive(course_id):
    return _course(course_id, "archive")


@app.route('/course/<course_id>', methods=['GET', 'POST'])
def course(course_id):
    return _course(course_id, "semester")


def _course(course_id, tab):
    course = Course.query.filter_by(id=course_id).first_or_404()

    resources_df = _fetch_resources(course_id, tab)
    if len(resources_df) == 0:
        return render_template('course.html', subjects=[], filtered_subject=[], course=course, current_search=request.form.get('query'), resources=dict())

    resources_df = _add_fake_rows(resources_df)
    all_subjects = _get_subjects(resources_df)

    resources_df = _filter_resources(resources_df, query=request.form.get(
        'query'), subject=request.form.getlist('subject'))

    if request.method == "POST":
        if current_user.is_authenticated:
            resources_df = _fetch_resources(course_id, tab)

            all_subjects = _get_subjects(resources_df)

            resources_df = _filter_resources(resources_df, query=request.form.get(
                'query'), subject=request.form.getlist('subject'))

    multi_resources = dict()
    if len(resources_df) > 0:
        for header in resources_df['header']:
            multi_resources[header] = resources_df[resources_df['header'] == header]

    return render_template('course.html', subjects=all_subjects, filtered_subjects=request.form.getlist('subject'), course=course, current_search=request.form.get('query'), resources=multi_resources, tab=tab)


@app.route('/updatecourse/<course_id>', methods=['GET', 'POST'])
def updatecourse(course_id):
    course = Course.query.filter_by(id=course_id).first_or_404()

    form = CourseResourcesForm()

    resources_df = _fetch_resources(course_id, "semester")
    archive_df = _fetch_resources(course_id, "archive")
    exams_df = _fetch_resources(course_id, "exams")

    if not form.validate_on_submit():
        form.resources.data = _resources_to_textarea(resources_df)
        form.archive.data = _resources_to_textarea(archive_df)
        form.exams.data = _resources_to_textarea(exams_df)
        return render_template('updatecourse.html', form=form, course=course)

    else:
        resources = [(line.split(' | ')[0], line.split(' | ')[1].split(' / ')[0], line.split(' | ')[1].split(' / ')[1], line.split(' | ')[1].split(' / ')[2] or None)
                     for line in form.resources.data.split('\r\n') if ' ' in line]
        archive = [(line.split(' | ')[0], line.split(' | ')[1].split(' / ')[0], line.split(' | ')[1].split(' / ')[1], line.split(' | ')[1].split(' / ')[2] or None)
                   for line in form.archive.data.split('\r\n') if ' ' in line]
        exams = [(line.split(' | ')[0], line.split(' | ')[1].split(' / ')[0], line.split(' | ')[1].split(' / ')[1], line.split(' | ')[1].split(' / ')[2] or None)
                 for line in form.exams.data.split('\r\n') if ' ' in line]

        db.session.query(ResourceToCourse).filter_by(
            course_id=course_id).delete()

        order_in_tab = 1
        for resource in resources:
            resource_to_course = ResourceToCourse(
                course_id=course_id, resource_id=resource[0], header=resource[1], rname=resource[2], rname_part=resource[3], tab="semester", order_in_tab=order_in_tab)
            db.session.add(resource_to_course)
            order_in_tab += 1

        order_in_tab = 1
        for resource in archive:
            resource_to_course = ResourceToCourse(
                course_id=course_id, resource_id=resource[0], header=resource[1], rname=resource[2], rname_part=resource[3], tab="archive", order_in_tab=order_in_tab)
            db.session.add(resource_to_course)
            order_in_tab += 1

        order_in_tab = 1
        for resource in exams:
            resource_to_course = ResourceToCourse(
                course_id=course_id, resource_id=resource[0], header=resource[1], rname=resource[2], rname_part=resource[3], tab="exams", order_in_tab=order_in_tab)
            db.session.add(resource_to_course)
            order_in_tab += 1

        db.session.commit()

        return render_template('updatecourse.html', form=form, course=course)


def _fetch_resources(course_id, tab):
    resource_to_course_df = pd.read_sql(ResourceToCourse.query.filter_by(
        course_id=course_id, tab=tab).statement, db.session.bind)

    if len(resource_to_course_df) == 0:
        return pd.DataFrame()

    resource_to_course_df.drop('id', axis=1, inplace=True)
    resource_to_course_df.drop('course_id', axis=1, inplace=True)
    resource_to_course_df.sort_values('order_in_tab', inplace=True)
    resource_ids = set(resource_to_course_df['resource_id'])

    resources_df = pd.read_sql(Resource.query.filter(
        Resource.id.in_(resource_ids)).statement, db.session.bind)

    resources_extended_df = resource_to_course_df
    if len(resources_df) > 0:
        resource_to_course_df.drop('tab', axis=1, inplace=True)
        resources_extended_df = pd.merge(how='right', left=resources_df, right=resource_to_course_df,
                                         left_on="id", right_on="resource_id").drop('resource_id', axis=1)
        resources_extended_df

    if current_user.is_authenticated:
        resource_to_user = pd.read_sql(ResourceToUser.query.filter_by(
            user_id=current_user.id).statement, db.session.bind)

        if len(resource_to_user) > 0:
            resource_to_user.drop('id', axis=1, inplace=True)
            resource_to_user.drop('user_id', axis=1, inplace=True)
            resources_extended_df = pd.merge(how='left',
                                             left=resources_extended_df, right=resource_to_user, left_on="id", right_on="resource_id").drop('resource_id', axis=1)

    if 'subject' in resources_extended_df.keys():
        resources_extended_df['subject'] = resources_extended_df['subject'].apply(
            lambda x: _jsonload(x))

    resources_extended_df = resources_extended_df.fillna(0)
    return resources_extended_df


def _add_fake_rows(resources_extended_df):
    resources_extended_df['is_fake_row'] = False

    resources_with_folded_rows = pd.DataFrame()
    folded_row_names = set()

    for index, row in resources_extended_df.iterrows():
        folded_row_name = row['rname']
        if row['rname_part'] and folded_row_name not in folded_row_names:
            folded_row_names.add(folded_row_name)
            folded_row = dict(row)
            folded_row['is_fake_row'] = True
            if 'done' in resources_extended_df.columns:
                folded_row['done'] = resources_extended_df[resources_extended_df['rname']
                                                           == folded_row_name]['done'].min()
            folded_row['subject'] = set([item for sublist in resources_extended_df[resources_extended_df['rname']
                                                                                   == folded_row_name]['subject'] for item in sublist])
            folded_row['textdump'] = ' '.join(resources_extended_df[resources_extended_df['rname']
                                                                    == folded_row_name]['textdump'])
            resources_with_folded_rows = resources_with_folded_rows.append(
                folded_row, ignore_index=True)
        resources_with_folded_rows = resources_with_folded_rows.append(
            row, ignore_index=True)

    resources_with_folded_rows['name_md5'] = resources_with_folded_rows['rname'].apply(
        lambda x: hashlib.md5(x.encode('utf-8')).hexdigest())
    return resources_with_folded_rows


def _jsonload(x):
    if isinstance(x, str):
        return json.loads(x)
    else:
        return ''


def _resources_to_textarea(df):
    return "\r\n".join(["{0} | {1} / {2} / {3}".format(
        resource.id, resource.header, resource.rname, resource.rname_part or '') for index, resource in df.iterrows()])


def _get_subjects(resources_df):
    list_of_lists = [
        resource[1].subject for resource in resources_df.iterrows()]
    return set([x for xs in list_of_lists for x in xs])


def _filter_resources(resources_extended_df, query, subject):
    if query and subject:
        resources_extended_df['show'] = (resources_extended_df['textdump'].str.contains(query.lower())) & (
            resources_extended_df['subject'].apply(lambda x: any([subj in x for subj in subject])))
    elif query:
        resources_extended_df['show'] = resources_extended_df['textdump'].str.contains(
            query.lower())
    elif subject:
        resources_extended_df['show'] = resources_extended_df['subject'].apply(
            lambda x: any([subj in x for subj in subject]))
    else:
        resources_extended_df['show'] = True

    if (query):
        resources_extended_df['occurrences'] = resources_extended_df['textdump'].str.count(
            query.lower())

    resources_extended_df = resources_extended_df[resources_extended_df['show']]

    return resources_extended_df


@ app.route('/updateresource', methods=['POST'])
def updateresource():
    resource_id = request.get_json()['resource_id']
    val = request.get_json()['val']

    if current_user.is_authenticated:
        db.session.query(ResourceToUser).filter_by(
            user_id=current_user.id, resource_id=resource_id).delete()

        resource_to_user = ResourceToUser(
            user_id=current_user.id, resource_id=resource_id, done=val)
        db.session.add(resource_to_user)
        db.session.commit()

    return render_template("index.html", title='Home Page')


@ app.route('/resource/<resource_id>', methods=['GET', 'POST'])
def resource(resource_id):
    resource = Resource.query.filter_by(id=resource_id).first_or_404()

    resource_tuples = []

    resource_descriptions = ResourceToCourse.query.filter_by(
        resource_id=resource_id).all()

    for res in resource_descriptions:
        course = Course.query.filter_by(id=res.course_id).first()
        resource_tuples += [(res.description.split('/')
                             [1], course.name, res.course_id)]

    return render_template('resource.html', resource=resource, resource_tuples=resource_tuples)


class Object(object):
    pass

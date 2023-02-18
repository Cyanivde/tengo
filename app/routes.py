from flask import redirect, url_for
from flask_login import logout_user

from app import app
from app.course import _course
from app.forgot_password import _forgot_password
from app.index import _index
from app.login import _login
from app.register import _register
from app.reset_password import _reset_password
from app.update_resource import _update_resource
from app.update_resource_to_user import _update_resource_to_user


@app.route('/')
def index():
    return _index()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return _register()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return _login()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return _forgot_password()


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    return _reset_password(token)


@app.route('/<course_institute>/<course_institute_id>/create_resource',
           methods=['GET', 'POST'])
def create_resource(course_institute, course_institute_id):
    return _update_resource(course_institute,
                            course_institute_id,
                            is_existing_resource=False)


@app.route('/<course_institute>/<course_institute_id>/edit_resource/<id>',
           methods=['GET', 'POST'])
def edit_resource(course_institute, course_institute_id, id=None):
    return _update_resource(course_institute,
                            course_institute_id,
                            is_existing_resource=True,
                            resource_id=id)


@ app.route('/updateresourcetouser', methods=['POST'])
def update_resource_to_user():
    return _update_resource_to_user()


@app.route('/<course_institute>/<course_institute_id>/<tab>', methods=['GET', 'POST'])
def course(course_institute, course_institute_id, tab):
    return _course(course_institute, course_institute_id, tab)


# TODO: remove this in ~30 days
@app.route('/<course_institute>/<course_institute_id>', methods=['GET', 'POST'])
def course_backwards_compatibility(course_institute, course_institute_id):
    return redirect(url_for("course", course_institute=course_institute, course_institute_id=course_institute_id, tab="lessons"))

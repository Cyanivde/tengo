from flask import render_template, request
from flask_login import current_user
from app.models import Course
from app.utils import _get_subjects, _fetch_resources


def _course(course_id, tab):
    course = Course.query.filter_by(course_id=course_id).first_or_404()

    resources_df = _fetch_resources(course_id, tab)
    if len(resources_df) == 0:
        return render_template('course.html', subjects=[], filtered_subject=[], course=course, resources=dict())

    # resources_df = _add_fake_rows(resources_df)
    all_subjects = _get_subjects(resources_df)

    if request.method == "POST":
        if current_user.is_authenticated:
            resources_df = _fetch_resources(course_id, tab)
            # resources_df = _add_fake_rows(resources_df)
            all_subjects = _get_subjects(resources_df)

    multi_resources = dict()
    if len(resources_df) > 0:
        for header in resources_df['header']:
            multi_resources[header] = resources_df[resources_df['header'] == header]

    return render_template('course.html', subjects=all_subjects, filtered_subjects=request.form.getlist('subject'), course=course, resources=multi_resources, tab=tab)

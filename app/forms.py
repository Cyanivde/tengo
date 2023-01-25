
from sqlite3 import Date
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Regexp, Optional

from app.models import User

ERR_EMPTY = "לא ניתן להשאיר ריק"


def strip_whitespace(s):
    if isinstance(s, str):
        s = s.strip()
    return s


class CourseResourcesForm(FlaskForm):
    resources = TextAreaField('חומרי הקורס')
    archive = TextAreaField('ארכיון חומרים')
    exams = TextAreaField('מבחנים')
    submit = SubmitField('שמירה')


class UpdateResourceForm(FlaskForm):
    type = SelectField('סוג',
                       choices=[
                           ('lecture', 'שיעור (הרצאה/תרגול/סדנה)'),
                           ('exercise_full', 'תרגיל בית'),
                           ('exercise', 'שאלה מתרגיל בית'),
                           ('exam_full', 'מבחן'),
                           ('exam', 'שאלה ממבחן'),
                           ('other', 'אחר (למשל סיכום אישי)')])
    display_name = StringField('שם תצוגה')
    questions_count = SelectField('כמה שאלות יש?', choices=range(1, 26))
    grouping = StringField('תיקייה')

    link = StringField('קישור', validators=[Regexp(r"^.*sharepoint\.com.*|\w{0}$", message="הקישור אינו תקין")])
    semester = SelectField(
        'סמסטר', choices=[
            ('חורף 2022-2023', 'חורף 2022-2023'),
            ('קיץ 2022', 'קיץ 2022'),
            ('אביב 2022', 'אביב 2022'),
            ('חורף 2021-2022', 'חורף 2021-2022'),
            ('קיץ 2021', 'קיץ 2021'),
            ('אביב 2021', 'אביב 2021'),
            ('חורף 2020-2021', 'חורף 2020-2021'),
            ('קיץ 2020', 'קיץ 2020'),
            ('אביב 2020', 'אביב 2020'),
            ('חורף 2019-2020', 'חורף 2019-2020'),
            ('קיץ 2019', 'קיץ 2019'),
            ('אביב 2019', 'אביב 2019'),
            ('חורף 2018-2019', 'חורף 2018-2019'),
            ('קיץ 2018', 'קיץ 2018'),
            ('אביב 2018', 'אביב 2018'),
            ('חורף 2017-2018', 'חורף 2017-2018'),
            ('קיץ 2017', 'קיץ 2017'),
            ('אביב 2017', 'אביב 2017'),
            ('חורף 2016-2017', 'חורף 2016-2017'),
            ('קיץ 2016', 'קיץ 2016'),
            ('אביב 2016', 'אביב 2016'),
            ('חורף 2015-2016', 'חורף 2015-2016'),
            ('קיץ 2015', 'קיץ 2015'),
            ('אביב 2015', 'אביב 2015'),
            ('חורף 2014-2015', 'חורף 2014-2015'),
            ('קיץ 2014', 'קיץ 2014'),
            ('אביב 2014', 'אביב 2014'),
            ('חורף 2013-2014', 'חורף 2013-2014'),
            ('קיץ 2013', 'קיץ 2013'),
            ('אביב 2013', 'אביב 2013'),
            ('חורף 2012-2013', 'חורף 2012-2013'),
            ('קיץ 2012', 'קיץ 2012'),
            ('אביב 2012', 'אביב 2012'),
            ('חורף 2011-2012', 'חורף 2011-2012'),
            ('קיץ 2011', 'קיץ 2011'),
            ('אביב 2011', 'אביב 2011'),
            ('חורף 2010-2011', 'חורף 2010-2011'),
            ('קיץ 2010', 'קיץ 2010'),
            ('אביב 2010', 'אביב 2010'),
            ('חורף 2009-2010', 'חורף 2009-2010'),
            ('קיץ 2009', 'קיץ 2009'),
            ('אביב 2009', 'אביב 2009'),
            ('חורף 2008-2009', 'חורף 2008-2009'),
            ('קיץ 2008', 'קיץ 2008'),
            ('אביב 2008', 'אביב 2008'),
            ('חורף 2007-2008', 'חורף 2007-2008'),
            ('קיץ 2007', 'קיץ 2007'),
            ('אביב 2007', 'אביב 2007'),
            ('חורף 2006-2007', 'חורף 2006-2007'),
            ('קיץ 2006', 'קיץ 2006'),
            ('אביב 2006', 'אביב 2006'),
            ('חורף 2005-2006', 'חורף 2005-2006'),
            ('קיץ 2005', 'קיץ 2005'),
            ('אביב 2005', 'אביב 2005'),
            ('חורף 2004-2005', 'חורף 2004-2005'),
            ('קיץ 2004', 'קיץ 2004'),
            ('אביב 2004', 'אביב 2004'),
            ('חורף 2003-2004', 'חורף 2003-2004'),
            ('קיץ 2003', 'קיץ 2003'),
            ('אביב 2003', 'אביב 2003'),
            ('חורף 2002-2003', 'חורף 2002-2003'),
            ('קיץ 2002', 'קיץ 2002'),
            ('אביב 2002', 'אביב 2002'),
            ('חורף 2001-2002', 'חורף 2001-2002'),
            ('קיץ 2001', 'קיץ 2001'),
            ('אביב 2001', 'אביב 2001'),
            ('חורף 2000-2001', 'חורף 2000-2001'),
            ('קיץ 2000', 'קיץ 2000'),
            ('אביב 2000', 'אביב 2000'),
        ],
        validate_choice=False)
    solution = StringField('קישור לפתרון', validators=[Regexp(r"^.*sharepoint\.com.*|\w{0}$", message="הקישור אינו תקין")])
    recording = StringField('קישורים להקלטות')
    recording2 = StringField('קישורים להקלטות')
    recording3 = StringField('קישורים להקלטות')
    recording4 = StringField('קישורים להקלטות')
    recording5 = StringField('קישורים להקלטות')
    recording_comment = StringField('הערה להקלטה')
    recording2_comment = StringField('הערה להקלטה')
    recording3_comment = StringField('הערה להקלטה')
    recording4_comment = StringField('הערה להקלטה')
    recording5_comment = StringField('הערה להקלטה')
    subject = StringField('נושאים (מופרדים בפסיק)')
    is_out_of_date = BooleanField('כבר לא בחומר')
    is_solution_partial = BooleanField('הפתרון חלקי')
    submit = SubmitField('שמירה')


class ForgotPasswordForm(FlaskForm):
    usernameemail = StringField('שם משתמש או כתובת מייל', filters=[strip_whitespace], validators=[
        DataRequired(message=ERR_EMPTY)])
    submit = SubmitField('שליחה')


class LoginForm(FlaskForm):
    usernameemail = StringField('שם משתמש או כתובת מייל', filters=[strip_whitespace], validators=[
        DataRequired(message=ERR_EMPTY)])
    password = PasswordField('סיסמה', validators=[
        DataRequired(message=ERR_EMPTY)])
    remember_me = BooleanField('זכור אותי')
    submit = SubmitField('התחברות')


class RegistrationForm(FlaskForm):
    username = StringField('username', filters=[strip_whitespace], validators=[
        DataRequired(message=ERR_EMPTY), Regexp(r"^\w{5,20}$", message=".שם המשתמש חייב להכיל 5-20 תווים: אותיות, ספרות או קו תחתון")])
    email = StringField('email', filters=[strip_whitespace], validators=[
        DataRequired(message=ERR_EMPTY),  Email(message="כתובת המייל אינה תקינה.")])
    password = PasswordField('password', validators=[
        DataRequired(message=ERR_EMPTY), Regexp('^(?=.*?[A-Za-z#?!@$%^&*-])(?=.*?[0-9]).{8,}$', message="הסיסמה חייבת להכיל 8 תווים לפחות, מהם לפחות אות אחת וספרה אחת.")])
    password2 = PasswordField(
        'confirm password', validators=[DataRequired(ERR_EMPTY), EqualTo('password')])
    submit = SubmitField('הרשמה')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user is not None:
            raise ValidationError('שם המשתמש כבר נמצא בשימוש.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user is not None:
            raise ValidationError('כתובת המייל כבר נמצאת בשימוש.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[
        DataRequired(message=ERR_EMPTY), Regexp('^(?=.*?[A-Za-z#?!@$%^&*-])(?=.*?[0-9]).{8,}$', message="הסיסמה חייבת להכיל 8 תווים לפחות, מהם לפחות אות אחת וספרה אחת.")])
    password2 = PasswordField(
        'confirm password', validators=[DataRequired(ERR_EMPTY), EqualTo('password')])
    submit = SubmitField('שמירה')

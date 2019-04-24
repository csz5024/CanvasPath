
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [validators.data_required()])

class PwReset(Form):
    user = StringField('Username', [validators.Length(min=1, max=50)])
    old = PasswordField('Current Password', [validators.data_required()])
    new = PasswordField('New Password', [validators.data_required()])
    confirm = PasswordField('Confirm Password', [validators.data_required()])

class addclass(Form):
    course_id = StringField('Course ID', [validators.Length(min=5, max=10)])
    course_name = StringField('Course Name', [validators.Length(min=5, max=100)])
    course_desc = StringField('Course Description', [validators.Length(min=5, max=100)])
    course_id2 = StringField('Course ID', [validators.Length(min=5, max=10)])
    prof_email = StringField('Professors Email', [validators.Length(min=5, max=100)])
    course_id3 = StringField('Course ID', [validators.Length(min=5, max=10)])
    sec_no = StringField('Section No', [validators.Length(min=0, max=5)])
    stud_email = StringField('Student Email', [validators.Length(min=5, max=100)])

class addFact(Form):
    username = StringField('Username', [validators.Length(min=5, max=10)])
    password = PasswordField('Password', [validators.data_required()])
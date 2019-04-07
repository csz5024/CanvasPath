
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [validators.data_required()])
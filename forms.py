from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, validators


class UserForm(FlaskForm):
    username = StringField('Username', validators=[
        validators.InputRequired(),
        validators.Length(min=4, max=25)])
    first_name = StringField('First name', validators=[
        validators.InputRequired(),
        validators.Length(min=3, max=25)])
    last_name = StringField('Last name', validators=[
        validators.InputRequired(),
        validators.Length(min=3, max=25)])
    phone = StringField('Phone', validators=[
        validators.InputRequired(),
        validators.Length(13)])
    email = EmailField('Email Address', validators=[
        validators.InputRequired(),
        validators.Length(min=6, max=35)])
    password = PasswordField('New Password', validators=[
        validators.InputRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

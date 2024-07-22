from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, validators


class UserForm(FlaskForm):
    username = StringField('Username', validators=[
        validators.InputRequired(),
        validators.Length(min=4, max=100)])
    first_name = StringField('First name', validators=[
        validators.InputRequired(),
        validators.Length(min=3, max=100)])
    last_name = StringField('Last name', validators=[
        validators.InputRequired(),
        validators.Length(min=3, max=100)])
    phone = StringField('Phone', validators=[
        validators.InputRequired(),
        validators.Length(13)])
    email = EmailField('Email Address', validators=[
        validators.InputRequired(),
        validators.Length(min=6, max=128)])
    password = PasswordField('New Password', validators=[
        validators.InputRequired(),
        validators.Length(min=8, max=128),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

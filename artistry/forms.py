from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from artistry.models import User
from flask_login import current_user
import secrets
import os


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm passowrd', validators=[DataRequired(), EqualTo('password')])

    checkterms = BooleanField('Creating an account means you’re okay with our Terms of Service, Privacy Policy, and our default Notification Settings.')

    submit = SubmitField('Join')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken!')

    def validate_password(self, password):
        if len(password.data) < 6:
            raise ValidationError('Password length must be 6+ character long.')
        else:
            return None


class LoginForm(FlaskForm):
    usernameOrEmail = StringField('Username or email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Log in')


class AccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = FileField('Upload your profile picture.', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'])])

    submit = SubmitField('Update')

    def validate_name(self, name):
        if name.data != current_user.name:
            user = User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError('Name is taken. Choose another one.')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken. Please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken choose another one')


#_____________ THE POST FORM __________#
class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    photo_file = FileField('Upload your craft', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'])])

    submit = SubmitField('Upload photo')


#___________ END POST FORM ____________#
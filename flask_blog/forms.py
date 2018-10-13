from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_blog.models import User

class RegistrationForm(FlaskForm): #To create a registration form, we make a registration form class
    '''
    This class is a registration form.
    'validators' ensure that the user input matches the specified criteria
    '''
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) #'Username' is the HTML label
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) #Equal to makes sure the passwords match
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user: #if username exists already, user is asked to choose a different username
            raise ValidationError('that username is taken. choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user: #if username exists already, user is asked to choose a different username
            raise ValidationError('that email is taken. choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm): #To create a registration form, we make a registration form class
    '''
    This class is a registration form.
    'validators' ensure that the user input matches the specified criteria
    '''
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) #'Username' is the HTML label
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update your information')

    def validate_username(self, username):
        '''If a user tries to update their username or email and submits the same username and email that they previously had,
           the program will throw an exception because it will see that a user with their username and email already exists in the
           database. For this reason, we only want to run the validation checks if the information the user submits to update their Username
           and email is different than their current username and email.
        '''
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first() #user will be NoneType if there are no users in the database with the username t
            if user: #if username exists already, user is asked to choose a different username
                raise ValidationError('that username is taken. choose a different one')

    def validate_email(self, email):
        '''If a user tries to update their username or email and submits the same username and email that they previously had,
           the program will throw an exception because it will see that a user with their username and email already exists in the
           database. For this reason, we only want to run the validation checks if the information the user submits to update their Username
           and email is different than their current username and email.
        '''
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user: #if username exists already, user is asked to choose a different username
                raise ValidationError('that email is taken. choose a different one')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

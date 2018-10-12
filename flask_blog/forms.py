from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
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

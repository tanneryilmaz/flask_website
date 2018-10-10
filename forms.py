from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField #this import lets you create string fields in your forms
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm): #To create a registration form, we make a registration form class
    '''
    This class is a registration form.
    'validators' ensure that the user input matches the specified criteria
    '''
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)]) #'Username' is the HTML label
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('Password')]) #Equal to makes sure the passwords match
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm): #To create a registration form, we make a registration form class
    ''' This class is a login form. '''
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

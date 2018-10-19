from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flask_blog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__) #instantiating a blueprint

@users.route("/register", methods=['GET', 'POST']) #we are adding the registration route to the 'users' blueprint object which is instantiated in this file
def register():
    if current_user.is_authenticated: #if user is already logged in and they click the link to the login page, they are redirected to the homepage
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #User() is a constructor for the User. We use this constructor to create a new instance of user in the database
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. Please log in', 'success') #success is a bootstrap class
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #if user is already logged in and they click the link to the login page, they are redirected to the homepage
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #the user is logged in if their password in database matches the password they entered into the login form
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else (url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm() #form object created for UpdateAccountForm
    #form.username.data refers to the data in the form in the username part of the form. current_user.username refers to the username of the current user in the database
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data #we are changing the current user's username in the database to whatever they entered the new username to be in the form.
        current_user.email = form.email.data
        db.session.commit() #adding user to database
        flash('your account info has been updated', 'success')
        return redirect(url_for('users.account')) #this line of code prevents the "post/get redirect pattern" from happening
    elif request.method == 'GET':
        form.username.data = current_user.username #filing in the username box in the form with the user's current username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file) #user's profile picture
    return render_template('account.html', title='Account', image_file=image_file, form=form) #form=form is how we pass the form object to the html page in which we want to display the form

@users.route("/user/<string:username>")
def user_post(username):
    '''in this function, we use the .paginate() method to split the posts into different pages'''
    page = request.args.get('page', 1, type=int) #the page number is set to the variable 'page'. default value for page number is '1'
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5) #posts variable is a pagination object. it holds all of the posts from the database. The posts are ordered so the most recent one is shown first

    return render_template('user_posts.html', posts=posts, user=user)



@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

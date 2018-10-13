import secrets
import os
from PIL import Image
from flask_blog.models import User, Post #this line must be after we create db variable
from flask import render_template, url_for, flash, redirect, request, abort
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm #these forms are used in each of the different web pages
from flask_blog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    '''in this function, we use the .paginate() method to split the posts into different pages'''
    page = request.args.get('page', 1, type=int) #the page number is set to the variable 'page'. default value for page number is '1'
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5) #posts variable is a pagination object. it holds all of the posts from the database. The posts are ordered so the most recent one is shown first
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: #if user is already logged in and they click the link to the login page, they are redirected to the homepage
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #User() is a constructor for the User. We use this constructor to create a new instance of user in the database
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. Please log in', 'success') #success is a bootstrap class
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #if user is already logged in and they click the link to the login page, they are redirected to the homepage
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #the user is logged in if their password in database matches the password they entered into the login form
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else (url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))




def save_picture(form_picture): #this method saves pictures that the user has uploaded to the database
    random_hex = secrets.token_hex(8) #creating a random hex code to use as a filename for the picture the user uploads
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) #explanation at 32:00 in tutorial #7 - we are defining the location where the picture will be saved

    output_size = (125,125) #in this block of code, we are resizing the image to a smaller size
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) #we are saving the image to the location of picture_path variable

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account')) #this line of code prevents the "post/get redirect pattern" from happening
    elif request.method == 'GET':
        form.username.data = current_user.username #filing in the username box in the form with the user's current username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file) #user's profile picture
    return render_template('account.html', title='Account', image_file=image_file, form=form) #form=form is how we pass the form object to the html page in which we want to display the form


@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) #giving information about the post to the post variable
        db.session.add(post) #adding post to database
        db.session.commit()  #adding post to database

        flash('Your post has been created!', 'success')
        return redirect(url_for('home')) #user is redirected to homepage if their post is successful
    return render_template('create_post.html', title='New Post', form = form, legend = 'New Post')

@app.route("/post/<int:post_id>", methods=['GET','POST']) #if user goes to url that ends with "/post/<int:post_id>", then the post with post_id = post_id is displayed
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required #user has to be logged in to change the content of a post
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit(): #if form is valid, update the title and content of the post with whatever is in the PostForm()
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id)) #'post' is a method and 'post_id' is the parameter it takes in
    elif request.method == 'GET':
        form.title.data = post.title #the form is populated with title of the post
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend = 'Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_post(username):
    '''in this function, we use the .paginate() method to split the posts into different pages'''
    page = request.args.get('page', 1, type=int) #the page number is set to the variable 'page'. default value for page number is '1'
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5) #posts variable is a pagination object. it holds all of the posts from the database. The posts are ordered so the most recent one is shown first

    return render_template('user_posts.html', posts=posts, user=user)

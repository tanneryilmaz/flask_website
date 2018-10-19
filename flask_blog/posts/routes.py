from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.models import Post
from flask_blog.posts.forms import PostForm

posts = Blueprint('posts', __name__) #instantiating a blueprint


@posts.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) #giving information about the post to the post variable
        db.session.add(post) #adding post to database
        db.session.commit()  #adding post to database

        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home')) #user is redirected to homepage if their post is successful
    return render_template('create_post.html', title='New Post', form = form, legend = 'New Post')

@posts.route("/post/<int:post_id>", methods=['GET','POST']) #if user goes to url that ends with "/post/<int:post_id>", then the post with post_id = post_id is displayed
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])
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
        return redirect(url_for('posts.post', post_id=post.id)) #'post' is a method and 'post_id' is the parameter it takes in
    elif request.method == 'GET':
        form.title.data = post.title #the form is populated with title of the post
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend = 'Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

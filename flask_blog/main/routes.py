from flask import render_template, request, Blueprint
from flask_blog.models import Post



main = Blueprint('main', __name__) #instantiating a blueprint


@main.route("/")
@main.route("/home")
def home():
    '''in this function, we use the .paginate() method to split the posts into different pages'''
    page = request.args.get('page', 1, type=int) #the page number is set to the variable 'page'. default value for page number is '1'
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5) #posts variable is a pagination object. it holds all of the posts from the database. The posts are ordered so the most recent one is shown first
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

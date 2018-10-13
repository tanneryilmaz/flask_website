'''this file holds the models for our database. models are basically
templates for database objects. For example, if I want to make a User object
in a database, I will create a model to structure the User'''

from flask_blog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    ''' This class defines structure of the User object. Each user of the website is put into the database as an instance of this User class'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) #grabs posts from the posts table by a specific author

    def __repr__(self):
        '''this method defines how the object is printed'''
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    ''' This class represents the structure of posts in the database'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False, default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #this is the id of the user that authored a posts

    def __repr__(self):
        '''this method defines how the object is printed'''
        return f"Post('{self.title}','{self.date_posted}')"

'''this file is where we initialize our application'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config


db = SQLAlchemy() #we have instantiated the database
bcrypt = Bcrypt()
login_manager=LoginManager()
login_manager.login_view = 'users.login' #when a page requires that the user be logged in to view it, the login manager will redirect the user to this specified route
login_manager.login_message_category = 'info' #adds a bootstrap style to the message that appears when we try to access a page that requires us to login
mail = Mail()

def create_app(config_class=Config): #Config is the configuration class that we created in the config.py file
    app = Flask(__name__)
    app.config.from_object(Config) #app's configuration variables are assigned using the variables defined in the Config.py file

    db.init_app(app) #db object is tied to this particular instance of the app. See tutorial 11, 33:00
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flask_blog.users.routes import users #we are importing the instance of the 'users' blueprint from the users/routes.py file
    from flask_blog.posts.routes import posts
    from flask_blog.main.routes import main
    from flask_blog.errors.handlers import errors #'errors' is the instance of the 'errors' blueprint which is instantiated in handlers.py
    app.register_blueprint(users) #we are registering the users blueprints with the app object
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)


    return app

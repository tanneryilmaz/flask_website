from flask import Flask
from flask import render_template #allows you to use html templates
from flask import url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'fd7fad7bc6cafe1f648eb630feea423c' #this is a passcode so people don't hack the website

posts = [
    #This list contains the dictionaries that contain the information we want to display on our website
    {
        'author': 'Tanner Yilmaz',
        'title': 'Blog Post 1',
        'content': 'Its a great day today',
        'date_posted': 'November 20, 2018'
    },
    {
        'author': 'Jake Gerber',
        'title': 'Blog Post 2',
        'content': 'Hello people of the world',
        'date_posted': 'November 21, 2018'
    }
]

@app.route("/") #this is the homepage path
@app.route("/home") #this is also the homepage path
def hello():
    return render_template('home.html', posts = posts) #'home.html is the html template file for the homepage'

@app.route("/about") #this is the about page
def about():
    return render_template('about.html', title = 'About') #the 'title' variable is passed to the html template

@app.route("/register") #this is the form page
def register():
    form = RegistrationForm() #form is an instance of the RegistrationForm
    return render_template('register.html', title='Register', form=form)

@app.route("/login") #this is the form page
def login():
    form = LoginForm() #form is an instance of the RegistrationForm
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)

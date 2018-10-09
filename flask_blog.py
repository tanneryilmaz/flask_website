from flask import Flask
from flask import render_template #allows you to use html templates
from flask import url_for
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)

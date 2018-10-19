# flask_website
Notes: This is a blog I am building using Flask. I am using Corey Schafer's tutorials for guidance. A link to his tutorials is provided below: https://www.youtube.com/watch?v=MwZwr5Tvyxo

-Any time you want to make a new page for your website, you must add that page's route to your routes.py file. Then you must create an HTML template for
that page in your Templates file. Then, if you want the page to have a form on it, you must create that form in the forms.py file. Then, you must import the form to your routes.py file and create an instance of the form in the route. Then, you must pass this instance into the render_template function as a parameter.

-In your HTML templates, you will want to add things such as buttons and text fields. You do this by creating those buttons and text fields in a class in the forms.py file. Then, lets say you want to put a button into your HTML in an HTML template file. Into your HTML, you write:
{{ form.submit(class="btn btn-outline-info") }}. This will add the submit variable from the form object. The form object is an instance of the
class which you defined in the routes.py file.

-models.py is the file that holds all of your database objects.

-layout.html is where we define what happens when we click on a button. For example, if we click on the "new post" link in the navbar, we are
redirected to the create_post.html page where we can create a new blog post.

-The routes.py file contains many functions. Inside of these functions, we show the user the HTML template using url_for().
We call these functions by using the following syntax: {{ url_for('posts.delete_post', post_id=post.id) }}. This syntax call's the 'posts.delete_post' method from
the routes.py file and passes in post.id as the method's argument.

-The pagination object called 'posts' in the route.py file holds all of the posts that are in our database. Storing the posts in this object makes it easier
to access the posts in a way that allows us to make our homepage have different pages.

-When you instantiate a blueprint, you can then pass routes to that blueprint instance. Then, when you create an app using the create_app() function, you register each of these blueprints with the instance of the app that you are creating. In my project, this is done in the flask_blog\__init__.py



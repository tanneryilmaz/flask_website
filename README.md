# flask_website
Notes:
-Any time you want to make a new page for your website, you must add that page's route to your routes.py file. Then you must create an HTML template for
that page in your Templates file. Then, if you want the page to have a form on it, you must create that form in the forms.py file. Then, you must import the form to your routes.py file and create an instance of the form in the route. Then, you must pass this instance into the render_template function as a parameter.

-In your HTML templates, you will want to add things such as buttons and text fields. You do this by creating those buttons and text fields in a class in the forms.py file. Then, lets say you want to put a button into your HTML in an HTML template file. Into your HTML, you write:
{{ form.submit(class="btn btn-outline-info") }}. This will add the submit variable from the form object. The form object is an instance of the
class which you defined in the routes.py file.

-Models.py is the file that holds all of your database objects.

-layout.html is where we define what happens when we click on a button. For example, if we click on the "new post" link in the navbar, we are
redirected to the create_post.html page where we can create a new blog post.

This is a blog I am building using Flask. I am using Corey Schafer's tutorials for guidance. A link to his tutorials is provided below:
https://www.youtube.com/watch?v=MwZwr5Tvyxo

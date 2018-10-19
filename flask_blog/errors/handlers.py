'''This file handles custom error pages. When an error is thrown, this file
is used to determine which custom error page is displayed'''


from flask import Blueprint, render_template


errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error): #this function decides which template is returned when an error is thrown. 
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail

def save_picture(form_picture): #this method saves pictures that the user has uploaded to the database
    random_hex = secrets.token_hex(8) #creating a random hex code to use as a filename for the picture the user uploads
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) #explanation at 32:00 in tutorial #7 - we are defining the location where the picture will be saved

    output_size = (125,125) #in this block of code, we are resizing the image to a smaller size
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) #we are saving the image to the location of picture_path variable

    return picture_fn


def send_reset_email(user): #sending email to user when they try to change their password
    token = user.get_reset_token()

    msg = Message('Password Reset Request',
                  sender= os.environ.get('email'),
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

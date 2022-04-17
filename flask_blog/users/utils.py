from flask import current_app, flash, url_for
from flask_blog import mongo, bcrypt, mail, aws3
from flask_login import current_user
from flask_blog.models import User
from PIL import Image
from bson import ObjectId
from flask_mail import Message
from itsdangerous import TimedSerializer as Serializer
import secrets
import os
import boto3


def create_username(fname, lname):
    # concat. fname & lname to generate generic username
    username = fname + "_" + lname
    # check if the generic username exist in DB
    user = list(mongo.db.users.find(
        {"username": {"$regex": username + '.*'}}).limit(1).sort("_id", -1))
    # if generic username exist add number at the end / incremente this nbr each time
    if len(user) > 0:
        splitId = user[0]["username"].split(username)[1]
        if splitId == "":
            newUsername = username + "1"
        else:
            lastUsernameID = str(
                int(user[0]["username"].split(username)[1]) + 1)
            newUsername = username + lastUsernameID
        return newUsername
    # return generic username
    else:
        return username


def save_picture(form_picture, type):
    # generate random file name 
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.data.filename)
    picture_fn = random_hex + f_ext
    
    # save the picture
    if type == "profile":
        picture_path = os.path.join(
            current_app.root_path, 'static/media/profile_pics', picture_fn)

        output_size = (300, 300)
        i = Image.open(form_picture.data)
        i.thumbnail(output_size)
        i.save(picture_path)
        
        
        acl="public-read" 
        dest = f'static/media/profile_pics/{picture_fn}'
        # #aws3.upload_fileobj(form_picture.data, 'nyplex-flask-blog',dest, ExtraArgs={ "ACL": acl, "ContentType": form_picture.data.content_type})
        
        with open(picture_path, "rb") as f:
            aws3.upload_fileobj(f, "nyplex-flask-blog", dest)
        
        if os.path.exists(picture_path):
            os.remove(picture_path)
        

        return picture_fn

    elif type == "postImage":
        picture_path = os.path.join(
            current_app.root_path, 'static/media/posts/pictures', picture_fn)
        i = Image.open(form_picture.data)
        i.save(picture_path)
        acl="public-read" 
        dest = f'static/media/posts/pictures/{picture_fn}'
        # aws3.upload_fileobj(form_picture.data, 'nyplex-flask-blog',dest, ExtraArgs={ "ACL": acl, "ContentType": form_picture.data.content_type} )
        
        with open(picture_path, "rb") as f:
            aws3.upload_fileobj(f, "nyplex-flask-blog", dest)
        
        if os.path.exists(picture_path):
            os.remove(picture_path)
        
        return "pictures/" + picture_fn


def validate_settings(form):
    upload_user = User(current_user)

    if form.username.data.strip() != "":
        upload_user.update({
            "username": form.username.data.strip()
        })
        form.username.data = ""
    if form.fname.data.strip() != "":
        upload_user.update({
            "fname": form.fname.data.strip()
        })
        form.fname.data = ""
    if form.lname.data.strip() != "":
        upload_user.update({
            "lname": form.lname.data.strip()
        })
        form.lname.data = ""
    if form.password.data.strip() != "":
        password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        upload_user.update({
            "password": password
        })
    if form.profile_pic.data:
        filename = save_picture(form.profile_pic, "profile")
        upload_user.update({
            "image": filename
        })

    newvalues = {"$set": upload_user}
    mongo.db.users.update_one(
        {"_id": ObjectId(current_user["_id"])}, newvalues)
    current_user.update(upload_user)

    flash("Your profile has been uptaded!", "flash-success")


def send_reset_email(user):
    expires_sec = 1800
    s = Serializer(current_app.config['SECRET_KEY'])
    userID = str(user['_id'])

    token = s.dumps({'user_id': userID})
    
    
    msg = Message('Password Reset Request',
                  sender='noreply@flaskblog.com', recipients=[user['email']])
    
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}
    
If you did not make this request, just ignore this email. 
    '''
    mail.send(msg)

def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return user

from flask import current_app, redirect, url_for, flash
from flask_blog import mongo, bcrypt
from flask_login import current_user
from flask_blog.models import User
from PIL import Image
from bson import ObjectId
import secrets
import os


def create_username(fname, lname):
    username = fname + "_" + lname
    user = list(mongo.db.users.find(
        {"username": {"$regex": username + '.*'}}).limit(1).sort("_id", -1))
    if len(user) > 0:
        splitId = user[0]["username"].split(username)[1]
        if splitId == "":
            newUsername = username + "1"
        else:
            lastUsernameID = str(
                int(user[0]["username"].split(username)[1]) + 1)
            newUsername = username + lastUsernameID
        return newUsername
    else:
        return username


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/media/profile_pics', picture_fn)

    # if current_user["image"] != "default.jpg":
    os.remove(os.path.join(current_app.root_path, 'static/media/profile_pics', current_user["image"]))
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


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
        filename = save_picture(form.profile_pic.data)
        upload_user.update({
            "image": filename
        })
    
    newvalues = { "$set": upload_user }
    mongo.db.users.update_one({"_id": ObjectId(current_user["_id"])}, newvalues)
    current_user.update(upload_user)

    flash("Your profile has been uptaded!", "flash-success")

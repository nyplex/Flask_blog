from flask_blog import mongo, bcrypt
from flask import Blueprint, current_app, redirect, request, render_template, url_for
from flask_blog.users.forms import SignupForm, LoginForm
from flask_blog.models import User
from datetime import datetime
from bson.objectid import ObjectId
from flask_blog.users.utils import create_username

users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("valid form")
    return render_template("login.html", title="FlaskBlog Login",
                           form=form)


@users.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    user = mongo.db.users.find_one({"email": "john.doe@gmail.com"})
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        fname = str(form.fname.data).lower()
        lname = str(form.lname.data).lower()
        username = create_username(fname, lname)
        newUser = User({
            "fname": fname,
            "lname": lname,
            "email": form.email.data,
            "username": username,
            "password": hashed_password,
            "image": "default.jpg",
            "signup_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
        newUser.save()
        return redirect(url_for("main.home"))
    return render_template("signup.html", title="FlaskBlog Register",
                           form=form, user=user)


@users.route("/logout")
def logout():
    return render_template("logout.html")


@users.route("/profile")
def profile():
    return render_template("profile.html", title="Profile")


@users.route("/settings")
def settings():
    return render_template("settings.html", title="Your Settings")

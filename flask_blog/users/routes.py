from flask_blog import mongo, bcrypt
from flask import Blueprint, redirect, request, render_template, url_for, flash
from flask_blog.users.forms import SignupForm, LoginForm, SettingsForm
from flask_blog.models import User
from datetime import datetime
from flask_blog.users.utils import create_username, validate_settings
from flask_login import login_user, current_user, logout_user

users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if form.validate_on_submit():
        # Find the using in the DB
        user = mongo.db.users.find_one({"email": form.email.data})
        # Check if user exists in DB AND if passwords match
        if user and bcrypt.check_password_hash(user["password"], form.password.data):
            login_user(User(user), remember=form.remember.data)
            flash("You are logged in!", "flash-success")
            # redirect user to his previous page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))

        flash("Wrong email or password", "flash-danger")

    return render_template("login.html", title="FlaskBlog Login",
                           form=form)


@users.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    # user = mongo.db.users.find_one({"email": "john.doe@gmail.com"})
    if form.validate_on_submit():
        # has password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # lower data
        fname = str(form.fname.data).lower()
        lname = str(form.lname.data).lower()
        username = create_username(fname, lname)

        # Create new User object using the data provided by user
        newUser = User({
            "fname": fname,
            "lname": lname,
            "email": form.email.data,
            "username": username,
            "password": hashed_password,
            "image": "default.jpg",
            "signup_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
        # Save new user in DB & log in him
        newUser.save()
        login_user(newUser)
        flash("Thanks for registered with us! You are now logged in.", "flash-success")
        return redirect(url_for("main.home"))

    return render_template("signup.html", title="FlaskBlog Register",
                           form=form)


@users.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You are logged out!", "flash-success")
    return redirect(url_for("users.login"))


@users.route("/profile", methods=["GET", "POST"])
def profile():
    ##########################################
    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
    ##########################################
    return render_template("profile.html", title="Profile", settingsForm=settingsForm)


@users.route("/users/<user_id>")
def single_user():
    ##########################################
    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
    ##########################################
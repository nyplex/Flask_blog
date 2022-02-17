from flask import Blueprint, current_app
from re import M
from flask import redirect, request, render_template, url_for
from flask_blog.users.forms import SignupForm, LoginForm
import os

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
    if form.validate_on_submit():
        print("valid form")
    return render_template("signup.html", title="FlaskBlog Register",
                           form=form)
    

@users.route("/logout")
def logout():
    return render_template("logout.html")


@users.route("/profile")
def profile():
    return render_template("profile.html", title="Profile")


@users.route("/settings")
def settings():
    return render_template("settings.html", title="Your Settings")
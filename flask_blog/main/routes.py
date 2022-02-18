from flask import Blueprint, current_app
from flask_blog import mongo
from flask import redirect, request, render_template, url_for
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
import os
from flask_blog.models import User

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html",
                           page_title="Home Page", active_link="home")

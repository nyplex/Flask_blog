from flask import Blueprint
from re import M
from flask import redirect, request, render_template, url_for
import os

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    # user = mongo.db.users.find_one({"email": "john.doe@gmail.com"})
    user = {
        "fname": "Alex",
        "lname": "doe"
    }
    return render_template("home.html", user=user,
                           page_title="Home Page", active_link="home")

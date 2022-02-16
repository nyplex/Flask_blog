from flask import redirect, request, render_template, url_for
from flask_blog import app, mongo
import os


@app.route("/")
@app.route("/home")
def home():
    user = mongo.db.users.find_one({"email": "john.doe@gmail.com"})
    return render_template("home.html", user=user, title="Home Page", active="home")


@app.route("/new-post")
def new_post():
    return render_template("new_post.html", title="New Post", active="new_post")

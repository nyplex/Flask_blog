from re import M
from flask import redirect, request, render_template, url_for
from flask_blog import app, mongo
import os


@app.route("/")
@app.route("/home")
def home():
    user = mongo.db.users.find_one({"email": "john.doe@gmail.com"})
    return render_template("home.html", user=user, 
                           page_title="Home Page", active_link="home")


@app.route("/new-post")
def new_post():
    return render_template("new_post.html", 
                           page_title="New Post", active_link="new_post")


@app.route("/categories")
def categories():
    return render_template("categories.html", 
                           page_title="Categories", active_link="categories")

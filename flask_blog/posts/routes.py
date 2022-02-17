from flask import Blueprint
from re import M
from flask import redirect, request, render_template, url_for
import os


posts = Blueprint("posts", __name__)


@posts.route("/new-post")
def new_post():
    return render_template("new_post.html",
                           page_title="New Post", active_link="new_post")


@posts.route("/categories")
def categories():
    return render_template("categories.html",
                           page_title="Categories", active_link="categories")
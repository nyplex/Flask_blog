from flask import Blueprint
from flask import redirect, request, render_template, url_for
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings


posts = Blueprint("posts", __name__)


@posts.route("/new-post", methods=["GET", "POST"])
def new_post():
    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
    return render_template("new_post.html",
                           page_title="New Post", active_link="new_post", 
                           settingsForm=settingsForm)


@posts.route("/categories", methods=["GET", "POST"])
def categories():
    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
    return render_template("categories.html",
                           page_title="Categories", active_link="categories", 
                           settingsForm=settingsForm)

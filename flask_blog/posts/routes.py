from flask import Blueprint, flash, redirect, request, render_template, url_for
from flask_login import login_required
from flask_blog import mongo
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings
from flask_blog.posts.forms import NewTopicForm
from flask_blog.posts.utils import saveNewTopic


posts = Blueprint("posts", __name__)


@posts.route("/new-post", methods=["GET", "POST"])
@login_required
def new_post():

    settingsForm = SettingsForm()
    newTopicForm = NewTopicForm()
    formCategories = mongo.db.categories.find().sort("category_name", 1)
    # Check if a form has been submited
    if request.method == "POST":
        # new post submit
        if "newPostSubmit" in request.form and newTopicForm.validate_on_submit():
            saveNewTopic(newTopicForm, request.form)
            flash("New Topic successfully posted!", "flash-success")
            return redirect(url_for("posts.new_post"))
        # update user settings submit
        elif "settingsSubmit" in request.form and settingsForm.validate_on_submit():
            validate_settings(settingsForm)
        # if forms are not validated flash message
        else:
            flash("There is an error in the form", "flash-danger")
    

    return render_template("new_post.html",
                           page_title="New Post", active_link="new_post", 
                           settingsForm=settingsForm, form=newTopicForm, categories=formCategories)


@posts.route("/categories", methods=["GET", "POST"])
def categories():
    ##########################################
    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
    ##########################################
    return render_template("categories.html",
                           page_title="Categories", active_link="categories", 
                           settingsForm=settingsForm)


@posts.route("/posts/<post_id>")
def single_post():
    ##########################################
    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
    ##########################################
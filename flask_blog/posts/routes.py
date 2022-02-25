from time import strftime
from flask import Blueprint, flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required
from flask_blog import mongo
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings
from flask_blog.posts.forms import NewTopicForm
from flask_blog.posts.utils import saveNewTopic, update_post_data
from bson import ObjectId
from datetime import datetime


posts = Blueprint("posts", __name__)


@posts.route("/new-post", methods=["GET", "POST"])
@login_required
def new_post():

    settingsForm = SettingsForm()
    newTopicForm = NewTopicForm(meta="hello")

    if request.method == "POST":
        if "newPostSubmit" in request.form and newTopicForm.validate_on_submit():
            saveNewTopic(newTopicForm, request.form)
            flash("New Topic successfully posted!", "flash-success")

            return redirect(url_for("posts.new_post"))

        elif "settingsSubmit" in request.form and settingsForm.validate_on_submit():
            validate_settings(settingsForm)
        else:
            flash("There is an error in the form", "flash-danger")

    return render_template("new_post.html",
                           page_title="New Post", active_link="new_post",
                           settingsForm=settingsForm, form=newTopicForm)


@posts.route("/categories", methods=["GET", "POST"])
def categories():

    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)

    return render_template("categories.html",
                           page_title="Categories", active_link="categories",
                           settingsForm=settingsForm)


@posts.route("/posts/<post_id>", methods=["GET", "POST"])
@login_required
def single_post(post_id):

    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)

    # get post from DB using post_id
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    posted_date = post['posted_date']
    update_post_data(post)
    post['posted_date'] = posted_date
    content = post['content']

    return render_template("post.html", post=post,
                           settingsForm=settingsForm, content=content)


@posts.route("/edit-post/<post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):

    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    update_post_data(post)
    settingsForm = SettingsForm()
    editTopicForm = NewTopicForm()
    if request.method == "POST":
        editTopicForm.topicBody.data = editTopicForm.topicBody.data
        editTopicForm.topicTitle.data = editTopicForm.topicTitle.data
        editTopicForm.categoryField.data = editTopicForm.categoryField.data
        
        if "newPostSubmit" in request.form and editTopicForm.validate_on_submit():
            print(editTopicForm.topicBody.data)
            flash("Edtit sucess", "flash-success")

        elif "settingsSubmit" in request.form and settingsForm.validate_on_submit():
            validate_settings(settingsForm)
        else:
            flash("There is an error in the form", "flash-danger")
    else:
        editTopicForm.topicBody.data = post['content']
        editTopicForm.topicTitle.data = post['title']
        editTopicForm.categoryField.data = post['category']['category_name']
        tagsList = post['tags']
        tags = ','.join(tagsList)
        editTopicForm.newTopicTags.data = tags

    return render_template("edit_post.html", settingsForm=settingsForm, 
                           form=editTopicForm)


@posts.route("/delete-post/<post_id>", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    update_post_data(post)
    if post['author']['_id'] != current_user._id:
        return redirect(url_for("posts.single_post", post_id=post_id))

    mongo.db.posts.delete_one({"_id": ObjectId(post_id)})
    return redirect(url_for("main.home"))

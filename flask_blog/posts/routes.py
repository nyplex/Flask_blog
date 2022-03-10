from time import strftime
from flask import Blueprint, flash, redirect, request, render_template, url_for, jsonify, make_response
from flask_login import current_user, login_required
from flask_blog import mongo
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings
from flask_blog.posts.forms import NewCommentForm, NewTopicForm
from flask_blog.posts.utils import saveNewTopic, update_post_data, edit_db_post, feel_post, dislike_post, love_post, update_comments_data
from flask_blog.models import Comments
from bson import ObjectId
from datetime import datetime
import re


posts = Blueprint("posts", __name__)


@posts.route("/new-post", methods=["GET", "POST"])
@login_required
def new_post():

    settingsForm = SettingsForm()
    newTopicForm = NewTopicForm()

    if request.method == "POST":
        if "newPostSubmit" in request.form and newTopicForm.validate_on_submit():
            saveNewTopic(newTopicForm)
            flash("New Topic successfully posted!", "flash-success")

            return redirect(url_for("posts.new_post"))

        elif "settingsSubmit" in request.form and settingsForm.validate_on_submit():
            validate_settings(settingsForm)
        else:
            flash("There is an error in the form", "flash-danger")

    return render_template("new_post.html",
                           page_title="New Post", active_link="new_post",
                           settingsForm=settingsForm, form=newTopicForm)


@posts.route("/posts/<post_id>", methods=["GET", "POST"])
@login_required
def single_post(post_id):

    commentForm = NewCommentForm()
    settingsForm = SettingsForm()
    if request.method == "POST":
        if "newCommentSubmit" in request.form and commentForm.validate_on_submit():
            
            newTopic = Comments({
            "author": current_user["_id"],
            "body": re.sub("\s\s+", " ", commentForm.commentBody.data),
            "posted_date": datetime.now(),
            "post": ObjectId(post_id)
            })
            mongo.db.comments.insert_one(newTopic)
            flash("Comment posted!", "flash-success")
            return redirect(url_for("posts.single_post", post_id=post_id))
            
        elif "settingsSubmit" in request.form and settingsForm.validate_on_submit():
            validate_settings(settingsForm)

    # get post from DB using post_id
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    comments = mongo.db.comments.find({"post": ObjectId(post_id)})
    posted_date = post['posted_date']
    update_post_data(post)
    update_comments = update_comments_data(comments)
    post['posted_date'] = posted_date
    content = post['content']
    return render_template("post.html", post=post,
                           settingsForm=settingsForm, 
                           content=content, comments=update_comments, 
                           form=commentForm)


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
            cat = mongo.db.categories.find_one(post['category'])
            count = cat["count"]
            mongo.db.categories.update_one(
                post['category'], {"$set": {"count": count - 1}})
            edit_db_post(editTopicForm, post_id)
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
                           form=editTopicForm, post_id=post_id)


@posts.route("/delete-post/<post_id>", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    cat = mongo.db.categories.find_one(ObjectId(post["category"]))
    count = cat["count"]
    mongo.db.categories.update_one(cat, {"$set": {"count": count - 1}})
    update_post_data(post)
    if post['author']['_id'] != current_user._id:
        return redirect(url_for("posts.single_post", post_id=post_id))

    mongo.db.posts.delete_one({"_id": ObjectId(post_id)})
    return redirect(url_for("main.home"))


@posts.route("/like-post/<post_id>/<feeling>", methods=["GET", "POST"])
@login_required
def like_post(post_id, feeling):

    if feeling == "like":
        feel_post(post_id, "like")
    elif feeling == "dislike":
        dislike_post(post_id, "dislike")
    elif feeling == "love":
        love_post(post_id, "love")

    return redirect(url_for("posts.single_post", post_id=post_id))


@posts.route("/delete-comment/<comment_id>/<post_id>", methods=["GET", "POST"])
@login_required
def delete_comment(comment_id, post_id):

    comment = mongo.db.comments.find_one({'_id': ObjectId(comment_id)})
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    if comment['author'] == current_user._id or post['author'] == current_user._id:
        mongo.db.comments.delete_one({"_id": ObjectId(comment_id)})
        flash("Comment deleted!", "flash-success")
        return redirect(url_for("posts.single_post", post_id=post_id))
    else:
        flash("You are not authorized to delete this comment!", "flash-danger")
        return redirect(url_for("posts.single_post", post_id=post_id))
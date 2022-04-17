from flask import Blueprint, flash, redirect, request, render_template, url_for, jsonify, make_response
from flask_login import current_user, login_required
from flask_blog import mongo
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings
from flask_blog.posts.forms import NewCommentForm, NewTopicForm
from flask_blog.posts.utils import saveNewTopic, update_post_data, edit_db_post, feel_post, dislike_post, love_post, update_comments_data
from flask_blog.models import Comments
from bson import ObjectId, json_util
import json
from datetime import datetime
import re
from flask_blog.errors.handlers import error_404


posts = Blueprint("posts", __name__)


@posts.route("/new-post", methods=["GET", "POST"])
@login_required
def new_post():

    settingsForm = SettingsForm()
    newTopicForm = NewTopicForm()

    if request.method == "POST":
        
        # validata the new post form 
        if "newPostSubmit" in request.form and newTopicForm.validate_on_submit():
            
            # save the the new post in DB
            saveNewTopic(newTopicForm)
            getPost = mongo.db.posts.find(
                {'author': ObjectId(current_user._id)}).sort("_id", -1).limit(1)
            
            #get the ID of the new post in order to redirect the url to this post
            postID = getPost[0]['_id']
            
            flash("New Topic successfully posted!", "flash-success")
            return redirect(url_for("posts.single_post", post_id=postID))

        #validate the settings form
        elif "settingsSubmit" in request.form and settingsForm.validate_on_submit():
            validate_settings(settingsForm)
            return redirect(url_for("posts.new_post"))
            
        #if one of the forms is not valid throw an error flash message
        else:
            flash("There is an error in the form", "flash-danger")
    
    page_data = {
        "title": "Create New Topic",
        "submit": "Create Topic"
    }

    return render_template("new_post.html",
                           page_title="New Post", active_link="new_post",
                           settingsForm=settingsForm, form=newTopicForm, page_data=page_data)


@posts.route("/posts/<post_id>", methods=["GET", "POST"])
@login_required
def single_post(post_id):
    
    commentForm = NewCommentForm()
    settingsForm = SettingsForm()
    
    if request.method == "POST":
        #validate the settings form
        if "settingsSubmit" in request.form and settingsForm.validate_on_submit():
            files = request.files.getlist('f[]')
            for f in files:
                print(len(f.read()))

            validate_settings(settingsForm)
            return redirect(url_for("posts.single_post", post_id=post_id))

        #validate new comment form
        elif commentForm.validate_on_submit():
            
            #save new comment in DB
            newTopic = Comments({
                "author": current_user["_id"],
                "body": re.sub("\s\s+", " ", commentForm.commentBody.data),
                "posted_date": datetime.now(),
                "post": ObjectId(post_id)
            })
            mongo.db.comments.insert_one(newTopic)
            
            #get the new comment from DB in order to send it back to the client via Ajax
            lastComment = mongo.db.comments.find({"author": ObjectId(
                current_user["_id"]), "body": re.sub("\s\s+", " ", commentForm.commentBody.data), "post": ObjectId(post_id)}).sort("posted_date", -1).limit(1)
            json_docs = [] #comment container
            result = {
                "_id": ObjectId(lastComment[0]['_id']),
                "author": current_user["_id"],
                "body": re.sub("\s\s+", " ", commentForm.commentBody.data),
                "posted_date": datetime.now(),
                "post": ObjectId(post_id)
            }
            #Comment Ajax Response
            dataArray = update_comments_data([result])
            json_doc = json.dumps(dataArray, default=json_util.default)
            json_docs.append(json_doc)

            return make_response(jsonify(json_docs))
        else:
            #error Ajax response
            return make_response(jsonify(False))
            
    # get post from DB using post_id from the URL
    try:
        post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
        comments = mongo.db.comments.find({"post": ObjectId(post_id)})
    except:
        return error_404("error")

    #Update and format post and comments 
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
    
    settingsForm = SettingsForm()
    editTopicForm = NewTopicForm()

    #Get the post to edit from DB
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    
    #Update and format the post
    update_post_data(post)
    
    if request.method == "POST":
        #Get the form content
        editTopicForm.topicBody.data = editTopicForm.topicBody.data
        editTopicForm.topicTitle.data = editTopicForm.topicTitle.data
        editTopicForm.categoryField.data = editTopicForm.categoryField.data

        #Validate the edit form content
        if "newPostSubmit" in request.form and editTopicForm.validate_on_submit():
            cat = mongo.db.categories.find_one(post['category'])
            
            #Update the 'count' on category in DB
            count = cat["count"]
            mongo.db.categories.update_one(
                post['category'], {"$set": {"count": count - 1}})
            
            #Edit the post and save it
            edit_db_post(editTopicForm, post_id)
            flash("Edtit sucess", "flash-success")
            return redirect(url_for("posts.single_post", post_id=post_id))

        #validate the settings form
        elif "settingsSubmit" in request.form and settingsForm.validate_on_submit():
            validate_settings(settingsForm)
            return redirect(url_for("posts.edit_post", post_id=post_id))
            
        #if one of the forms is not valid throw an error flash message
        else:
            flash("There is an error in the form", "flash-danger")
    
    #Populate the editPost form
    else:
        editTopicForm.topicBody.data = post['content']
        editTopicForm.topicTitle.data = post['title']
        editTopicForm.categoryField.data = post['category']['category_name']
        tagsList = post['tags']
        tags = ','.join(tagsList)
        editTopicForm.newTopicTags.data = tags
    
    page_data = {
        "title": "Edit Topic",
        "submit": "Edit Post"
    }

    return render_template("new_post.html", settingsForm=settingsForm,
                           form=editTopicForm, post_id=post_id, page_data=page_data)


@posts.route("/delete-post/<post_id>", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    
    #Get the post to delete
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    
    #Get the category and update the count
    cat = mongo.db.categories.find_one(ObjectId(post["category"]))
    count = cat["count"]
    mongo.db.categories.update_one(cat, {"$set": {"count": count - 1}})
    
    #Format and update post
    update_post_data(post)
    
    # if user is NOT authorized to delete the post
    if post['author']['_id'] != current_user._id and current_user.fname != "admin":
        return redirect(url_for("posts.single_post", post_id=post_id))

    # delete post
    mongo.db.posts.delete_one({"_id": ObjectId(post_id)})
    flash("Post succesfully deleted", "flash-success")
    
    return redirect(url_for("main.home"))


@posts.route("/like-post/<post_id>/<feeling>", methods=["GET", "POST"])
@login_required
def like_post(post_id, feeling):

    #Update the feelings
    if feeling == "like":
        feel_post(post_id, "like")
    elif feeling == "dislike":
        dislike_post(post_id, "dislike")
    elif feeling == "love":
        love_post(post_id, "love")

    #Get the post from DB
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    
    #Update and format post
    update_post_data(post)
    
    #Store the feeling's data of the post
    data = {
        "like": post['like'],
        "dislike": post['dislike'],
        "love": post['love']
    }

    return make_response(jsonify(data))


@posts.route("/delete-comment/<comment_id>/<post_id>", methods=["GET", "POST"])
@login_required
def delete_comment(comment_id, post_id):

    #Get post and comment from DB
    comment = mongo.db.comments.find_one({'_id': ObjectId(comment_id)})
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})

    #Check if user is authorized to delete the comment
    if comment['author'] == current_user._id or post['author'] == current_user._id or current_user.username == "admin":
        mongo.db.comments.delete_one({"_id": ObjectId(comment_id)})
        return make_response("deleted")
    
    #throw a flash message if user is not authorized to delete the comment and redirect to the post
    else:
        flash("You are not authorized to delete this comment!", "flash-danger")
        return redirect(url_for("posts.single_post", post_id=post_id))


@posts.route("/load-comments", methods=["GET", "POST"])
@login_required
def load_comments():
    
    json_docs = [] #data container
    
    if request.method == "POST":
        post_id = request.values.get('postID')
        counter = int(request.values.get('c'))
        if counter >= 1:
            counter -= 1
        limit = int(request.values.get('limit'))
        #Get comments fron DB
        comments = mongo.db.comments.find(
            {"post": ObjectId(post_id)}).sort("posted_date", 1).skip(counter).limit(limit)
        dataLen = len(list(mongo.db.comments.find({"post": ObjectId(post_id)}).skip(counter).limit(limit)))
        total = len(list(mongo.db.comments.find({"post": ObjectId(post_id)})))

    #Update and format comments
    for comment in comments:
        dataArray = update_comments_data([comment])
        json_doc = json.dumps(dataArray, default=json_util.default)
        json_docs.append(json_doc)

    #Store the data to return
    result = {
        "result": json_docs,
        "counts": dataLen,
        "total": total
    }

    return make_response(jsonify(result))

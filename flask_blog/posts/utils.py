from collections import defaultdict
from datetime import datetime
from flask import current_app
from flask_blog import mongo
from flask_login import current_user
from flask_blog.models import Post
from flask_blog.users.utils import save_picture
from bson import ObjectId
import secrets
import os
import re


def format_post_date(postDate):
    then = postDate
    now = datetime.now()
    duration = now - then
    duration_in_s = duration.total_seconds()

    years = divmod(duration_in_s, 31536000)[0]
    days = divmod(duration_in_s, 86400)[0]
    hours = divmod(duration_in_s, 3600)[0]
    minutes = divmod(duration_in_s, 60)[0]
    if years > 0:
        return str(int(years)) + "y"
    if days > 0:
        return str(int(days)) + "d"
    if hours > 0:
        return str(int(hours)) + "h"
    if minutes > 0:
        return str(int(minutes)) + "m"
    if duration_in_s > 30:
        return str(int(duration_in_s)) + "s"
    if duration_in_s > 0:
        return "now"
    return "now"


def saveTopicVideo(video):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(video.filename)
    video_fn = random_hex + f_ext
    # save the file
    picture_path = os.path.join(
        current_app.root_path, 'static/media/posts/videos', video_fn)
    video.save(picture_path)

    return "videos/" + video_fn


def saveNewTopic(form):
    category_id = mongo.db.categories.find_one(
        {"category_name": form.categoryField.data})
    tags = form.newTopicTags.data
    tagsList = tags.split(",")
    if tagsList == [""]:
        tagsList = []

    # if user input media
    if form.topicMedia.data:
        postMedia = form.topicMedia.data
        # get the file extension
        _, f_ext = os.path.splitext(postMedia.filename)
        if f_ext in [".png", ".jpg", ".jpeg"]:
            filename = save_picture(form.topicMedia.data, "postImage")
        else:
            filename = saveTopicVideo(form.topicMedia.data)
    else:
        filename = None

    # Create new Post object to save inDB
    newTopic = Post({
        "author": current_user["_id"],
        "title": re.sub("\s\s+", " ", form.topicTitle.data),
        "content": form.topicBody.data,
        "posted_date": datetime.now(),
        "like": 0,
        "category": category_id["_id"],
        "tags": tagsList,
        "media": filename,
        "dislike": 0,
        "love": 0,
        "comments": []
    })
    cat = mongo.db.categories.find_one(category_id)
    count = cat["count"]
    mongo.db.categories.update_one(category_id, {"$set":{"count": count + 1}})
    mongo.db.posts.insert_one(newTopic)


def edit_db_post(form, post_id):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    category_id = mongo.db.categories.find_one(
        {"category_name": form.categoryField.data})
    
    tags = form.newTopicTags.data
    tagsList = tags.split(",")
    if tagsList == [""]:
        tagsList = []
    # if user input media
    if form.topicMedia.data:
        postMedia = form.topicMedia.data
        # get the file extension
        _, f_ext = os.path.splitext(postMedia.filename)
        if f_ext in [".png", ".jpg", ".jpeg"]:
            filename = save_picture(form.topicMedia.data, "postImage")
        else:
            filename = saveTopicVideo(form.topicMedia.data)
    else:
        filename = None
    # Create new Post object to save inDB
    mongo.db.posts.update_one(post, {"$set": {
        "title": re.sub("\s\s+", " ", form.topicTitle.data),
        "content": form.topicBody.data,
        "category": category_id["_id"],
        "tags": tagsList,
        "media": filename
    }})

def update_posts_data(posts):
    updated_posts = []

    for post in posts:
        # get author and category of each post from DB using their ID
        post["author"] = mongo.db.users.find_one(ObjectId(post["author"]))
        post["category"] = mongo.db.categories.find_one(ObjectId(post["category"]))
        post["posted_date"] = format_post_date(post["posted_date"])

        updated_posts.append(post)
    
    for updated_post in updated_posts:
        removeKey = ["password", "email", "signup_date"]
        for key in removeKey:
            del updated_post["author"][key]
                
    return updated_posts


def update_post_data(post):
    postArray = []
    post["author"] = mongo.db.users.find_one(ObjectId(post["author"]))
    post["category"] = mongo.db.categories.find_one(ObjectId(post["category"]))
    post["posted_date"] = format_post_date(post["posted_date"])
    
    #Update the new post array with the updated post 
    postArray.append(post)
    # remove user private data before sending it back to the Ajax call
    removeKey = ["password", "email", "signup_date"]
    for key in removeKey:
        del postArray[0]["author"][key]
        
    return postArray
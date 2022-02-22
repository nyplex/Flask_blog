from datetime import datetime
from flask import current_app
from flask_blog import mongo
from flask_login import current_user
from flask_blog.models import Post
from flask_blog.users.utils import save_picture
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
    # generate random key
    random_hex = secrets.token_hex(8)
    # get the picture file name
    _, f_ext = os.path.splitext(video.filename)
    # concat. random key + pic. file extension
    video_fn = random_hex + f_ext
    # save the file
    picture_path = os.path.join(
        current_app.root_path, 'static/media/posts/videos', video_fn)
    video.save(picture_path)
    # return the file name
    return "videos/" + video_fn


def saveNewTopic(form, form2):
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
        "media": filename
    })

    mongo.db.posts.insert_one(newTopic)

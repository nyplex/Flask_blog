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
    # Get the time diff. between now and when the topic was posted
    
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
            filename = save_picture(form.topicMedia, "postImage")
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
        "category": category_id["_id"],
        "tags": tagsList,
        "media": filename,
        "like": 0,
        "liked_by": [],
        "dislike": 0,
        "disliked_by": [],
        "love": 0,
        "loved_by": [],
        "comments": []
    })
    #Get category and update count
    cat = mongo.db.categories.find_one(category_id)
    count = cat["count"]
    mongo.db.categories.update_one(category_id, {"$set":{"count": count + 1}})
    
    #Save the new post
    mongo.db.posts.insert_one(newTopic)


def edit_db_post(form, post_id):
    
    #Get the post to edit
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    
    #get the cateogry of the post
    category_id = mongo.db.categories.find_one(
        {"category_name": form.categoryField.data})
    
    #Get the tags
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
        filename = post['media']
        
    # Create new Post object to save inDB
    mongo.db.posts.update_one(post, {"$set": {
        "title": re.sub("\s\s+", " ", form.topicTitle.data),
        "content": form.topicBody.data,
        "category": category_id["_id"],
        "tags": tagsList,
        "media": filename
    }})
    
    #Update category count
    cat = mongo.db.categories.find_one(category_id)
    count = cat["count"]
    
    #Update the post
    mongo.db.categories.update_one(category_id, {"$set":{"count": count + 1}})


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


def update_comments_data(comments):
    updated_comments = []
    
    for comment in comments:
        # get author and category of each post from DB using their ID
        comment["author"] = mongo.db.users.find_one(ObjectId(comment["author"]))
        comment["posted_date"] = format_post_date(comment["posted_date"])
        post = mongo.db.posts.find_one({"_id": ObjectId(comment['post'])})
        
        if comment['author']['_id'] == current_user._id or post['author'] == current_user._id or current_user.username == "admin":
            comment["delete"] = True
        else:
            comment["delete"] = False
            
        updated_comments.append(comment)
    
    for updated_comment in updated_comments:
        removeKey = ["password", "email", "signup_date"]
        for key in removeKey:
            del updated_comment["author"][key]
                
    return updated_comments


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



def feel_post(post_id, feeling):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    dislike = post['dislike']
    disliked_by = post['disliked_by']
    love = post['love']
    loved_by = post['loved_by']
    
    if current_user._id in post['disliked_by']:
        dislike = post['dislike'] -1
        disliked_by = post['disliked_by']
        disliked_by.remove(current_user['_id'])
    
    if current_user._id in post['loved_by']:
        love = post['love'] -1
        loved_by = post['loved_by']
        loved_by.remove(current_user['_id'])
        
    if current_user._id in post["liked_by"]:
        like = post['like'] - 1
        likedBy = post['liked_by']
        likedBy.remove(current_user["_id"])
    else:
        like = post['like'] + 1
        likedBy = post['liked_by']
        likedBy.append(current_user["_id"])

    mongo.db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": {
        "like": like,
        "liked_by": likedBy,
        "dislike": dislike,
        "disliked_by": disliked_by,
        "love": love,
        "loved_by": loved_by
    }})


def dislike_post(post_id, feeling):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    like = post['like']
    liked_by = post['liked_by']
    love = post['love']
    loved_by = post['loved_by']
    
    if current_user._id in post['liked_by']:
        like = post['like'] -1
        liked_by = post['liked_by']
        liked_by.remove(current_user['_id'])
    
    if current_user._id in post['loved_by']:
        love = post['love'] -1
        loved_by = post['loved_by']
        loved_by.remove(current_user['_id'])
        
    if current_user._id in post["disliked_by"]:
        dislike = post['dislike'] - 1
        disliked_by = post['disliked_by']
        disliked_by.remove(current_user["_id"])
    else:
        dislike = post['dislike'] + 1
        disliked_by = post['disliked_by']
        disliked_by.append(current_user["_id"])

    mongo.db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": {
        "like": like,
        "liked_by": liked_by,
        "dislike": dislike,
        "disliked_by": disliked_by,
        "love": love,
        "loved_by": loved_by
    }})


def love_post(post_id, feeling):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    like = post['like']
    liked_by = post['liked_by']
    dislike = post['dislike']
    disliked_by = post['disliked_by']
    
    if current_user._id in post['liked_by']:
        like = post['like'] -1
        liked_by = post['liked_by']
        liked_by.remove(current_user['_id'])
    
    if current_user._id in post['disliked_by']:
        dislike = post['dislike'] -1
        disliked_by = post['disliked_by']
        disliked_by.remove(current_user['_id'])
        
    if current_user._id in post["loved_by"]:
        love = post['love'] - 1
        loved_by = post['loved_by']
        loved_by.remove(current_user["_id"])
    else:
        love = post['love'] + 1
        loved_by = post['loved_by']
        loved_by.append(current_user["_id"])

    mongo.db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": {
        "like": like,
        "liked_by": liked_by,
        "dislike": dislike,
        "disliked_by": disliked_by,
        "love": love,
        "loved_by": loved_by
    }})
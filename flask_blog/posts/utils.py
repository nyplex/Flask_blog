from datetime import datetime
from flask import flash
from flask_blog import mongo
from flask_login import current_user
from flask_blog.models import Post
from flask_blog.users.utils import save_picture

def format_post_date(postDate):
        then = postDate
        now  = datetime.now() 
        duration = now - then
        duration_in_s = duration.total_seconds() 
        
        years = divmod(duration_in_s, 31536000)[0]
        days  = divmod(duration_in_s, 86400)[0]
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


def saveNewTopic(form, form2):
    category_id = mongo.db.categories.find_one({"category_name": form2.get("newTopicCategory")})
    tags = form.newTopicTags.data
    tagsList = tags.split(",")
    if form.topicMedia.data:
        filename = save_picture(form.topicMedia.data)
    else: 
        filename = None
    newTopic = Post({
        "author": current_user["_id"],
        "title": form.topicTitle.data,
        "content": form.topicBody.data,
        "posted_date": datetime.now(),
        "like": 0,
        "category": category_id["_id"],
        "tags": tagsList,
        "media": filename
    })
    
    mongo.db.posts.insert_one(newTopic)
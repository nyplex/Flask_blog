from flask import Blueprint, request, render_template, jsonify, make_response
from flask_blog import mongo
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings
from flask_blog.posts.utils import update_posts_data, update_post_data
from bson import ObjectId, json_util
import json

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():

    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
        
        
    posts = mongo.db.posts.find().sort("posted_date", -1).limit(5)
    updated_post = update_posts_data(posts)

    return render_template("home.html",
                           page_title="Home Page", active_link="home", 
                           settingsForm=settingsForm, posts=updated_post)



@main.route("/load")
def load():
    """ Route to load the posts on the home page => Ajax call"""
    #check is args in url
    if request.args:
        counter = int(request.args.get("c"))  # The 'counter' value sent in the URL by Ajax call
        postsLength = len(list(mongo.db.posts.find())) # Total of posts in the DB
        posts = mongo.db.posts.find().skip(5).sort("posted_date", -1).skip(counter).limit(5) # load post skip by counter and limit to 5
        json_docs = []
        
        for post in posts:
            postArray = update_post_data(post)
            # Convert data to json format
            json_doc = json.dumps(postArray, default=json_util.default)
            json_docs.append(json_doc)
        # Add data and total of post and return to Ajax call
        result = {
            "result": json_docs,
            "total": postsLength
        }
        res = make_response(jsonify(result))

    return res




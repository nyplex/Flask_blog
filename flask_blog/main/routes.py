from flask import Blueprint, current_app
from flask_blog import mongo
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings
from flask import redirect, request, render_template, url_for
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from bson import ObjectId
from datetime import datetime
from flask_blog.main.utils import format_post_date

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    ##########################################
    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
    ##########################################
    
    # Get post from DB
    posts = mongo.db.posts.find().sort("posted_date", -1)
    updated_post = []
    for post in posts:
        author = mongo.db.users.find_one(ObjectId(post["author"]))
        category = mongo.db.categories.find_one(ObjectId(post["category"]))
        post["author"] = author
        post["category"] = category
        newDate = format_post_date(post["posted_date"])
        post["posted_date"] = newDate
        
        updated_post.append(post)
        
    return render_template("home.html",
                           page_title="Home Page", active_link="home", 
                           settingsForm=settingsForm, posts=updated_post)

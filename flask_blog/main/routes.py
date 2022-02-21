from flask import Blueprint, request, render_template
from flask_blog import mongo
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings
from flask_blog.posts.utils import format_post_date
from bson import ObjectId

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    ##########################################
    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
    ##########################################
    if request.method == "GET" and request.args.get('sort'):
        posts = mongo.db.posts.find().sort(request.args.get('sort'), 1)
    else:
        posts = mongo.db.posts.find().sort("posted_date", -1)
    
    # Create a new array containing all the posts with the formated data.
    updated_post = []
    for post in posts:
        # get author and category of each post from DB using their ID
        author = mongo.db.users.find_one(ObjectId(post["author"]))
        category = mongo.db.categories.find_one(ObjectId(post["category"]))
        # update each post with the Author and Category object
        post["author"] = author
        post["category"] = category
        # get the difference between current time and posted_date of each post
        newDate = format_post_date(post["posted_date"])
        # update the post date 
        post["posted_date"] = newDate
        # append the updated post to the new array
        updated_post.append(post)
        
    return render_template("home.html",
                           page_title="Home Page", active_link="home", 
                           settingsForm=settingsForm, posts=updated_post)

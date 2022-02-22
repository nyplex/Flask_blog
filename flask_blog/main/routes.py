from flask import Blueprint, request, render_template, jsonify, make_response
from flask_blog import mongo
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings
from flask_blog.posts.utils import format_post_date
from bson import ObjectId, json_util
import json

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    ##########################################
    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
    ##########################################

    posts = mongo.db.posts.find().sort("posted_date", -1).limit(5)
    
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



@main.route("/load")
def load():
    """ Route to load the posts """

    if request.args:
        counter = int(request.args.get("c"))  # The 'counter' value sent in the QS
        
        posts = mongo.db.posts.find().skip(5).sort("posted_date", -1).skip(counter).limit(5)
        json_docs = []
        
        for post in posts:
            postArray = []
            post["author"] = mongo.db.users.find_one(ObjectId(post["author"]))
            post["category"] = mongo.db.categories.find_one(ObjectId(post["category"]))
            post["posted_date"] = format_post_date(post["posted_date"])
        
            postArray.append(post)
            removeKey = ["password", "email", "signup_date"]
            for key in removeKey:
                del postArray[0]["author"][key]

            json_doc = json.dumps(postArray, default=json_util.default)
            json_docs.append(json_doc)
    
        res = make_response(jsonify(json_docs))
        
        # if counter == 0:
        #     print(f"Returning posts 0 to {quantity}")
        #     # Slice 0 -> quantity from the db
        #     res = make_response(jsonify(db[0: quantity]), 200)

        # elif counter == posts:
        #     print("No more posts")
        #     res = make_response(jsonify({}), 200)

        # else:
        #     print(f"Returning posts {counter} to {counter + quantity}")
        #     # Slice counter -> quantity from the db
        #     res = make_response(jsonify(db[counter: counter + quantity]), 200)

    return res




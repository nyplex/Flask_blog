from flask import Blueprint, request, render_template, jsonify, make_response, current_app
from flask_blog import mongo
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings
from flask_blog.posts.utils import update_posts_data, update_post_data
from bson import ObjectId, json_util
from flask_login import login_required
import json

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
@main.route("/categories/<category_id>", methods=["GET", "POST"])
@login_required
def home(**category_id):

    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
    if category_id:
        category = mongo.db.categories.find_one({"_id": ObjectId(category_id['category_id'])})
        posts = mongo.db.posts.find({"category": ObjectId(category_id['category_id'])}).sort(
            "posted_date", -1).limit(5)
        data_category = category["category_name"]
        liveSearchCategory = category["_id"]
        updated_post = update_posts_data(posts)

    else:
        data_category = "multi"
        liveSearchCategory = "liveSearchCategory"
        posts = mongo.db.posts.find().sort("posted_date", -1).limit(5)
        updated_post = update_posts_data(posts)

    

    return render_template("home.html",
                           page_title="Home Page", active_link="home",
                           settingsForm=settingsForm, posts=updated_post, data_category=data_category, liveSearchCategory=liveSearchCategory)


@main.route("/categories", methods=["GET", "POST"])
@login_required
def categories():

    categories = mongo.db.categories.find().sort("category_name", 1).limit(6)
    # add count to DB & update count when del. post
    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)

    return render_template("categories.html",
                           page_title="Categories", active_link="categories",
                           settingsForm=settingsForm, categories=categories)


@main.route("/load", methods=["GET"])
@login_required
def load_data():

    limit = 6
    json_docs = []

    if request.args:
        counter = int(request.args.get("c"))
        collection = str(request.args.get("coll"))

        if collection == "posts":
            category = str(request.args.get("category"))
            if category == "multi":
                dataLen = len(list(mongo.db.posts.find()))
                datas = mongo.db.posts.find().skip(limit).sort("posted_date", -1).skip(counter).limit(limit)
            else:
                categoryId = mongo.db.categories.find_one({"category_name": category})
                dataLen = len(list(mongo.db.posts.find({"category": ObjectId(categoryId["_id"])})))
                datas = mongo.db.posts.find({"category": ObjectId(categoryId["_id"])}).skip(limit).sort("posted_date", -1).skip(counter).limit(limit)
                
        elif collection == "categories":
            dataLen = len(list(mongo.db.categories.find()))
            datas = mongo.db.categories.find().skip(limit).sort(
                "category_name", 1).skip(counter).limit(limit)

        for data in datas:
            if collection == "posts":
                dataArray = update_post_data(data)
            elif collection == "categories":
                dataArray = data

            json_doc = json.dumps(dataArray, default=json_util.default)
            json_docs.append(json_doc)

        result = {
            "result": json_docs,
            "total": dataLen
        }

    return make_response(jsonify(result))


@main.route("/live-search", methods=["GET", "POST"])
@login_required
def live_search():
    json_docs = []
    if request.method == "POST":
        data = request.values.get('input')
        liveSearchCategory = request.values.get('liveSearchCategory')
        liveSearchUser = request.values.get('liveSearchUser')
        print(liveSearchUser)

        if liveSearchUser == "all":
            if liveSearchCategory == "liveSearchCategory":
                if data == "":
                    posts = mongo.db.posts.find().sort("posted_date", -1).limit(5)
                else:
                    posts = mongo.db.posts.find({"title": {"$regex": data, "$options" :'i'}}).sort("posted_date", -1).limit(5)
            else:
                if data == "":
                    posts = mongo.db.posts.find({"category": ObjectId(liveSearchCategory)}).sort("posted_date", -1).limit(5)
                else:
                    posts = mongo.db.posts.find({"title": {"$regex": data, "$options" :'i'}, "category": ObjectId(liveSearchCategory)}).sort("posted_date", -1).limit(5)
        else:
            if liveSearchCategory == "liveSearchCategory":
                if data == "":
                    posts = mongo.db.posts.find({"author": ObjectId(liveSearchUser)}).sort("posted_date", -1).limit(5)
                else:
                    posts = mongo.db.posts.find({"title": {"$regex": data, "$options" :'i'}, 'author': ObjectId(liveSearchUser)}).sort("posted_date", -1).limit(5)
            else:
                if data == "":
                    posts = mongo.db.posts.find({"category": ObjectId(liveSearchCategory), "author": ObjectId(liveSearchUser)}).sort("posted_date", -1).limit(5)
                else:
                    posts = mongo.db.posts.find({"title": {"$regex": data, "$options" :'i'}, "category": ObjectId(liveSearchCategory), "author": ObjectId(liveSearchUser)}).sort("posted_date", -1).limit(5)

        
        for data in posts:
            dataArray = update_post_data(data)
            json_doc = json.dumps(dataArray, default=json_util.default)
            json_docs.append(json_doc)
        
    return make_response(jsonify(json_docs))

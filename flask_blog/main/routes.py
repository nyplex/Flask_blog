from calendar import c
from flask import Blueprint, redirect, request, render_template, jsonify, make_response, current_app, url_for, flash
from flask_blog import mongo
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings
from flask_blog.posts.utils import update_posts_data, update_post_data
from flask_blog.posts.forms import NewCategoryForm
from bson import ObjectId, json_util
from flask_login import login_required, current_user
import json
import random

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
@main.route("/categories/<category_id>", methods=["GET", "POST"])
@login_required
def home(**category_id):

    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
        if category_id:
            return redirect(url_for("main.home", category_id=category_id))
        else:
            return redirect(url_for("main.home"))

    # Load posts by category
    if category_id:
        category = mongo.db.categories.find_one(
            {"_id": ObjectId(category_id['category_id'])})
        posts = mongo.db.posts.find({"category": ObjectId(category_id['category_id'])}).sort(
            "posted_date", -1).limit(5)
        data_category = category["category_name"]
        countResult = f"" + \
            str(len(list(mongo.db.posts.find(
                {"category": ObjectId(category_id['category_id'])}))))
        liveSearchCategory = category["_id"]
        updated_post = update_posts_data(posts)

    # Load all posts
    else:
        data_category = "multi"
        category = None
        liveSearchCategory = "liveSearchCategory"
        posts = mongo.db.posts.find().sort("posted_date", -1).limit(5)
        updated_post = update_posts_data(posts)
        countResult = f"" + str(len(list(mongo.db.posts.find())))

    return render_template("home.html",
                           page_title="Flask Blog", active_link="home",
                           settingsForm=settingsForm, posts=updated_post,
                           data_category=data_category,
                           liveSearchCategory=liveSearchCategory,
                           countResult=countResult, category=category)


@main.route("/categories", methods=["GET", "POST"])
@login_required
def categories():

    categories = mongo.db.categories.find().sort("category_name", 1).limit(6)
    settingsForm = SettingsForm()
    newCategoryForm = NewCategoryForm()

    if request.method == "POST":

        # validata the new category form
        if "newCategorySubmit" in request.form and newCategoryForm.validate_on_submit():
            
            colors = ["yellow", "purple", "pink", "orange", "red", "cyan", "amber",
                      "indigo", "violet", "sky", "emerald", "lime", "teal", "gray"]
            rdmColor = random.choice(colors)
            category_name = newCategoryForm.categoryName.data
            category_description = newCategoryForm.categoryDescription.data
            
            mongo.db.categories.insert_one({
                "category_name": category_name.lower(),
                "category_color": rdmColor,
                "count": 0,
                "description": category_description.capitalize()
            })
            # save the the new category in DB

            flash("New Category successfully created!", "flash-success")
            return redirect(url_for("main.categories"))

        # validate the edit category form
        elif "editCategorySubmit" in request.form and newCategoryForm.validate_on_submit():
            category_id = request.form.get('editCategoryID')
            
            mongo.db.categories.update_one({"_id": ObjectId(category_id)}, {"$set": {
                "category_name": newCategoryForm.categoryName.data,
                "description": newCategoryForm.categoryDescription.data
            }})
            
            flash("Category successfully edited!", "flash-success")
            return redirect(url_for("main.categories"))

        # validate the settings form
        elif "settingsSubmit" in request.form and settingsForm.validate_on_submit():
            validate_settings(settingsForm)
            return redirect(url_for("main.categories"))

        # if one of the forms is not valid throw an error flash message
        else:
            flash("There is an error in the form", "flash-danger")

    return render_template("categories.html",
                           page_title="Categories", active_link="categories",
                           settingsForm=settingsForm, categories=categories,
                           newCategoryForm=newCategoryForm)


@main.route("/delete-categories/<category_id>", methods=["GET", "POST"])
@login_required
def delete_categories(category_id):
    # Get post and comment from DB
    category = mongo.db.categories.find_one({'_id': ObjectId(category_id)})

    # Check if user is authorized to delete the comment
    if current_user.username == "admin":
        mongo.db.categories.delete_one({"_id": ObjectId(category_id)})
        mongo.db.posts.delete_many({"category": ObjectId(category_id)})
        flash("Category Deleted!", "flash-success")
        return redirect(url_for("main.categories"))

    # throw a flash message if user is not authorized to delete the comment and redirect to the post
    else:
        flash("You are not authorized to delete a category!", "flash-danger")
        return redirect(url_for("main. "))


@main.route("/load", methods=["GET"])
@login_required
def load_data():

    limit = 5  # limit of post to load per call
    json_docs = []  # data containers

    if request.args:
        # get the paramets passed in the URL when firing Ajax call
        counter = int(request.args.get("c"))
        collection = str(request.args.get("coll"))
        userID = request.args.get("userid")

        # check if to load posts content
        if collection == "posts":
            category = str(request.args.get("category"))

            # load all posts
            if category == "multi":
                dataLen = len(list(mongo.db.posts.find()))
                datas = mongo.db.posts.find().skip(limit).sort(
                    "posted_date", -1).skip(counter).limit(limit)

            # load post but filter by category
            else:
                categoryId = mongo.db.categories.find_one(
                    {"category_name": category})
                dataLen = len(list(mongo.db.posts.find(
                    {"category": ObjectId(categoryId["_id"])})))
                datas = mongo.db.posts.find({"category": ObjectId(categoryId["_id"])}).skip(
                    limit).sort("posted_date", -1).skip(counter).limit(limit)

        elif collection == "postUser":
            category = str(request.args.get("category"))

            # load all posts
            if category == "multi":
                dataLen = len(list(mongo.db.posts.find(
                    {"author": ObjectId(userID)})))
                datas = mongo.db.posts.find({"author": ObjectId(userID)}).skip(limit).sort(
                    "posted_date", -1).skip(counter).limit(limit)

            # load post but filter by category
            else:
                categoryId = mongo.db.categories.find_one(
                    {"category_name": category})
                dataLen = len(list(mongo.db.posts.find(
                    {"category": ObjectId(categoryId["_id"]), "author": ObjectId(userID)})))
                datas = mongo.db.posts.find({"category": ObjectId(categoryId["_id"]), "author": ObjectId(userID)}).skip(
                    limit).sort("posted_date", -1).skip(counter).limit(limit)

        # check if to load categories content
        elif collection == "categories":
            dataLen = len(list(mongo.db.categories.find()))
            datas = mongo.db.categories.find().skip(limit).sort(
                "category_name", 1).skip(counter).limit(limit)

        # update & format data
        for data in datas:
            if collection == "posts" or collection == "postUser":
                dataArray = update_post_data(data)
            elif collection == "categories":
                dataArray = data

            json_doc = json.dumps(dataArray, default=json_util.default)
            json_docs.append(json_doc)

            if current_user.username == "admin":
                delete = True
            else:
                delete = False

        result = {
            "result": json_docs,
            "total": dataLen,
            "delete": delete
        }

    return make_response(jsonify(result))


@main.route("/live-search", methods=["GET", "POST"])
@login_required
def live_search():

    json_docs = []  # data container
    limit = 5  # limit of data to load during live saerch

    if request.method == "POST":
        data = request.values.get('input')
        liveSearchCategory = request.values.get('liveSearchCategory')
        liveSearchUser = request.values.get('liveSearchUser')

        # live search on all users
        if liveSearchUser == "all":

            # live search on all posts
            if liveSearchCategory == "liveSearchCategory":
                if data == "":
                    posts = mongo.db.posts.find().sort("posted_date", -1).limit(limit)
                    dataLen = len(list(mongo.db.posts.find()))
                else:
                    posts = mongo.db.posts.find({"title": {"$regex": data, "$options": 'i'}}).sort(
                        "posted_date", -1).limit(limit)
                    dataLen = len(list(mongo.db.posts.find({"title": {"$regex": data, "$options": 'i'}}).sort(
                        "posted_date", -1).limit(limit)))

            # live search on posts filter by category
            else:
                if data == "":
                    posts = mongo.db.posts.find({"category": ObjectId(liveSearchCategory)}).sort(
                        "posted_date", -1).limit(limit)
                    dataLen = len(list(mongo.db.posts.find(
                        {"category": ObjectId(liveSearchCategory)})))
                else:
                    posts = mongo.db.posts.find({"title": {"$regex": data, "$options": 'i'}, "category": ObjectId(
                        liveSearchCategory)}).sort("posted_date", -1).limit(limit)
                    dataLen = len(list(mongo.db.posts.find({"title": {"$regex": data, "$options": 'i'}, "category": ObjectId(
                        liveSearchCategory)}).sort("posted_date", -1).limit(limit)))

        # live search on a specific user
        else:

            # live search on all posts
            if liveSearchCategory == "liveSearchCategory":
                if data == "":
                    posts = mongo.db.posts.find({"author": ObjectId(liveSearchUser)}).sort(
                        "posted_date", -1).limit(limit)
                    dataLen = len(list(mongo.db.posts.find(
                        {"author": ObjectId(liveSearchUser)})))
                else:
                    posts = mongo.db.posts.find({"title": {"$regex": data, "$options": 'i'}, 'author': ObjectId(
                        liveSearchUser)}).sort("posted_date", -1).limit(limit)
                    dataLen = len(list(mongo.db.posts.find({"title": {"$regex": data, "$options": 'i'}, 'author': ObjectId(
                        liveSearchUser)}).sort("posted_date", -1).limit(limit)))

            # live search on posts filter by category
            else:
                if data == "":
                    posts = mongo.db.posts.find({"category": ObjectId(liveSearchCategory), "author": ObjectId(
                        liveSearchUser)}).sort("posted_date", -1).limit(limit)
                    dataLen = len(list(mongo.db.posts.find({"category": ObjectId(liveSearchCategory), "author": ObjectId(
                        liveSearchUser)})))
                else:
                    posts = mongo.db.posts.find({"title": {"$regex": data, "$options": 'i'}, "category": ObjectId(
                        liveSearchCategory), "author": ObjectId(liveSearchUser)}).sort("posted_date", -1).limit(limit)
                    dataLen = len(list(mongo.db.posts.find({"title": {"$regex": data, "$options": 'i'}, "category": ObjectId(
                        liveSearchCategory), "author": ObjectId(liveSearchUser)}).sort("posted_date", -1).limit(limit)))

        for data in posts:
            dataArray = update_post_data(data)
            json_doc = json.dumps(dataArray, default=json_util.default)
            json_docs.append(json_doc)

        response = {
            "data": json_docs,
            "total": dataLen
        }

    return make_response(jsonify(response))

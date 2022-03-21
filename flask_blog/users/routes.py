from flask_blog import mongo, bcrypt
from flask import Blueprint, redirect, request, render_template, url_for, flash
from flask_blog.users.forms import SignupForm, LoginForm, SettingsForm, RequestResetPassword, ResetPassword
from flask_blog.models import User
from datetime import datetime
from flask_blog.users.utils import create_username, send_reset_email, validate_settings, verify_reset_token
from flask_blog.posts.utils import update_posts_data, update_post_data
from flask_login import login_user, current_user, logout_user, login_required
from bson import ObjectId

users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if form.validate_on_submit():
        # Find the using in the DB
        user = mongo.db.users.find_one({"email": form.email.data})
        # Check if user exists in DB AND if passwords match
        if user and bcrypt.check_password_hash(user["password"], form.password.data):
            login_user(User(user), remember=form.remember.data)
            flash("You are logged in!", "flash-success")
            # redirect user to his previous page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))

        flash("Wrong email or password", "flash-danger")

    return render_template("login.html", page_title="FlaskBlog Login",
                           form=form)


@users.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    # user = mongo.db.users.find_one({"email": "john.doe@gmail.com"})
    if form.validate_on_submit():
        # has password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # lower data
        fname = str(form.fname.data).lower()
        lname = str(form.lname.data).lower()
        username = create_username(fname, lname)

        # Create new User object using the data provided by user
        newUser = User({
            "fname": fname,
            "lname": lname,
            "email": form.email.data,
            "username": username,
            "password": hashed_password,
            "image": "default.jpg",
            "signup_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
        # Save new user in DB & log in him
        newUser.save()
        login_user(newUser)
        flash("Thanks for registered with us! You are now logged in.", "flash-success")
        return redirect(url_for("main.home"))

    return render_template("signup.html", page_title="FlaskBlog Register",
                           form=form)


@users.route("/reset-password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RequestResetPassword()
    
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"email": form.email.data})
        send_reset_email(user)
        flash('An email has been sent to reset your password', "flash-success")
        return redirect(url_for("users.login"))
    
    return render_template("reset_request.html", page_title="Reset Password", form=form)


@users.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    user = verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "danger")
        return redirect(url_for("users.reset_request"))
    
    form = ResetPassword()
    
    if form.validate_on_submit():
        # has password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        
        mongo.db.users.update_one(user, {"$set": {"password": hashed_password}})

        flash("Your password has been updated!", "flash-success")
        return redirect(url_for("users.login"))
    
    return render_template("reset_password.html", page_title="Reset Password", form=form)
    
    

@users.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You are logged out!", "flash-success")
    return redirect(url_for("users.login"))


@users.route("/profile/<user_id>", methods=["GET", "POST"])
@users.route("/profile/<user_id>/categories/<category_id>", methods=["GET", "POST"])
@login_required
def profile(user_id, **category_id):

    # Get the user from DB
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    postsCount = len(list(mongo.db.posts.find({"author": ObjectId(user_id)})))

    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)
        if category_id:
            return redirect(url_for("users.profile", user_id=user_id, category_id=category_id))
        else:
            return redirect(url_for("users.profile", user_id=user_id))
        

    # Load post filtered by category if cat. param. exists
    if category_id:
        category = mongo.db.categories.find_one(
            {"_id": ObjectId(category_id['category_id'])})
        posts = mongo.db.posts.find({"author": ObjectId(user_id), "category": ObjectId(
            category_id['category_id'])}).sort("posted_date", -1).limit(5)

        data_category = category["category_name"]
        countResult = f"" + str(len(list(mongo.db.posts.find({"category": ObjectId(category_id['category_id']), "author": ObjectId(user_id)}))))
        liveSearchCategory = category["_id"]
        updated_post = update_posts_data(posts)

    # Load all the user's posts
    else:
        category = None
        data_category = "multi"
        liveSearchCategory = "liveSearchCategory"
        posts = mongo.db.posts.find({"author": ObjectId(user_id)}).sort(
            "posted_date", -1).limit(5)
        countResult = f"" + str(len(list(mongo.db.posts.find({"author": ObjectId(user_id)}))))
        updated_post = update_posts_data(posts)

    return render_template("profile.html", page_title="Profile",
                           settingsForm=settingsForm, user=user,
                           postsCount=postsCount, posts=updated_post, 
                           liveSearchUser=user_id, 
                           liveSearchCategory=liveSearchCategory, 
                           profile=True, data_category=data_category, countResult=countResult, category=category)

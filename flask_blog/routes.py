from flask import redirect, request, render_template, url_for
from flask_blog import app, mongo
import os


@app.route("/")
@app.route("/home")
def home():
    user = mongo.db.users.find_one({"email": "john.doe@gmail.com"})
    print(str(user))
    return render_template("home.html", user=user)

from flask import redirect, request, render_template, url_for
from flask_blog import app, mongo
import os


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

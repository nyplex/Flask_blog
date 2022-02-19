from flask import Blueprint, current_app
from flask_blog import mongo
from flask_blog.users.forms import SettingsForm
from flask_blog.users.utils import validate_settings
from flask import redirect, request, render_template, url_for
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    settingsForm = SettingsForm()
    if settingsForm.validate_on_submit():
        validate_settings(settingsForm)

    return render_template("home.html",
                           page_title="Home Page", active_link="home", 
                           settingsForm=settingsForm)

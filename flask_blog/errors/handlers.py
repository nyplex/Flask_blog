from flask import Blueprint, render_template
from flask_blog.users.forms import SettingsForm

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    settingsForm = SettingsForm()
    return render_template('errors/404.html', settingsForm=settingsForm), 404


@errors.app_errorhandler(403)
def error_403(error):
    settingsForm = SettingsForm()
    return render_template('errors/403.html', settingsForm=settingsForm), 403


@errors.app_errorhandler(500)
def error_500(error):
    settingsForm = SettingsForm()
    return render_template('errors/500.html', settingsForm=settingsForm), 500
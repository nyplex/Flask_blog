import os
from flask import Flask
if os.path.exists("env.py"):
    import env
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_blog.config import Config
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor


mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = "flash-danger"
bcrypt = Bcrypt()
ckeditor = CKEditor()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    ckeditor.init_app(app)

    from flask_blog.users.routes import users
    from flask_blog.posts.routes import posts
    from flask_blog.main.routes import main
    from flask_blog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

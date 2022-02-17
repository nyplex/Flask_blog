import os
from flask import Flask
if os.path.exists("env.py"):
    import env
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_blog.config import Config



# app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
# app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(tls=True, tlsAllowInvalidCertificates=True)
# login_manager = LoginManager()
# login_manager.login_view = 'users.login'







def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    mongo.init_app(app)
    # login_manager.init_app(app)

    from flask_blog.users.routes import users
    from flask_blog.posts.routes import posts
    from flask_blog.main.routes import main
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
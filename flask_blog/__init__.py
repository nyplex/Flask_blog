import os
from flask import Flask
if os.path.exists("env.py"):
    import env
from flask_pymongo import PyMongo
from flask_login import LoginManager


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app, tls=True, tlsAllowInvalidCertificates=True)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'


from flask_blog import routes





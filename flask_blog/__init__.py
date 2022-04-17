import os
from flask import Flask
if os.path.exists("env.py"):
    import env
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_blog.config import Config
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_s3 import FlaskS3
import boto3, botocore


mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = "flash-danger"
bcrypt = Bcrypt()
ckeditor = CKEditor()
mail = Mail()
s3 = FlaskS3()
aws3 = boto3.client(
    "s3",
    aws_access_key_id='AKIA3OBQOA4ILHM23YFM',
    aws_secret_access_key='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'
    )


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.config['FLASKS3_BUCKET_NAME'] = 'nyplex-flask-blog'
    app.config['FLASKS3_REGION'] = 'eu-west-2'
    app.config['AWS_ACCESS_KEY_ID'] = 'AKIA3OBQOA4ILHM23YFM'
    app.config['AWS_SECRET_ACCESS_KEY'] = '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'
    
    app.config['S3_BUCKET'] = "nyplex-flask-blog"
    app.config['S3_KEY'] = "AKIA3OBQOA4ILHM23YFM"
    app.config['S3_SECRET'] = "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"
    app.config['S3_LOCATION'] = 'eu-west-2'

    
    mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get('EMAIL_USER'),
    "MAIL_PASSWORD": os.environ.get('EMAIL_PASSWORD')
    }
    app.config.update(mail_settings)
    
    mongo.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    s3.init_app(app)

    from flask_blog.users.routes import users
    from flask_blog.posts.routes import posts
    from flask_blog.main.routes import main
    from flask_blog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

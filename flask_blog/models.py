from flask_blog import mongo, login_manager
from model.pymongo_model import SimpleModel


@login_manager.user_loader
def load_user(email):
    user = mongo.db.users.find_one({"email": email})
    if user:
        return User(user)
    return None


class User(SimpleModel):
    collection = mongo.db.users

    def is_authenticated():
        return True

    def is_active():
        return True

    def is_anonymous():
        return False

    def get_id(self):
        return self.email


class Post(SimpleModel):
    collection = mongo.db.posts
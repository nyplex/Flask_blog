from flask_blog import mongo


def create_username(fname, lname):
    username = fname + "_" + lname
    user = mongo.db.users.find(
        {"username": {"$regex": username + '.*'}}).limit(1).sort("_id", -1)
    if len(list(user)) != 0:
        lastUsernameID = str(int(user[0]["username"].split(username)[1]) + 1)
        newUsername = username + lastUsernameID
        return newUsername
    else:
        return username

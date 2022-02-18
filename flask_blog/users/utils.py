from flask_blog import mongo


def create_username(fname, lname):
    username = fname + "_" + lname
    user = list(mongo.db.users.find(
        {"username": {"$regex": username + '.*'}}).limit(1).sort("_id", -1))
    if len(user) > 0:
        splitId = user[0]["username"].split(username)[1]
        if splitId == "":
            newUsername = username + "1"
        else:
            lastUsernameID = str(int(user[0]["username"].split(username)[1]) + 1)
            newUsername = username + lastUsernameID
        return newUsername
    else:
        return username

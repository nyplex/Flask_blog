from flask_blog import mongo


def create_username(fname, lname):
    """Generate an username by concatenate fname and lname. 
    Check in DB if that username already exists.
    If it does, append a number to username. 

    Args:
        fname (string): user's first name
        lname (string): user's last name

    Returns:
        string: return user's UNIQUE username
    """
    username = fname + "_" + lname
    user = list(mongo.db.users.find(
        {"username": {"$regex": username + '.*'}}).limit(1).sort("_id", -1))
    if len(user) > 0:
        splitId = user[0]["username"].split(username)[1]
        if splitId == "":
            newUsername = username + "1"
        else:
            lastUsernameID = str(
                int(user[0]["username"].split(username)[1]) + 1)
            newUsername = username + lastUsernameID
        return newUsername
    else:
        return username

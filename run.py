from flask_blog import app
import os

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=True)
from flask_blog import create_app
import os

app = create_app()

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=False)
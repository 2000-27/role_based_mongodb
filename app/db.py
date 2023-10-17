from flask_pymongo import PyMongo
import os


def init_db():
    mongo = PyMongo()
    return mongo


def get_db(app, mongo):
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    mongo.init_app(app)


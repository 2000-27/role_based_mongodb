from flask_pymongo import PyMongo

def init_db():
    mongo = PyMongo()
    return mongo

def get_db(app, mongo):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/my_db"
    mongo.init_app(app)
  
   

    


from flask_pymongo import PyMongo

def init_db():
    mongo = PyMongo()
    return mongo

def get_db(app, mongo):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/my_db"
    mongo.init_app(app)
    collist = mongo.db.list_collection_names()
    if 'role' not in collist :
            mongo.db.role.insert_many([
        {
            "id":1,
            "role_name":"ADMIN"
        },
        {
            "id":2,
            "role_name":"MANAGER"
        },
        {
            "id":3,
            "role_name":"USER"
        }, 
        ])

   

    


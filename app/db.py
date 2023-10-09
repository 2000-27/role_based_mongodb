from flask_pymongo import PyMongo
from flask_mail import Mail


def init_db():
    mongo = PyMongo()
    return mongo


def init_mail():
    mail = Mail()
    return mail


def get_db(app, mongo, mail):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/my_db"

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'jangid2000neetu@gmail.com'
    app.config['MAIL_PASSWORD'] = 'lvxz vcbi moqz pfxk'
    app.config['MAIL_USE_TLS'] = True
   
    mail.init_app(app)
    mongo.init_app(app)

from flask_mail import Mail
from dotenv import load_dotenv
import os 

load_dotenv()


def init_mail():
    mail = Mail()
    return mail


def get_mail(app, mail):
    app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
    app.config['MAIL_PORT'] = os.environ.get("MAIL_PORT")
    app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD") 
    app.config['MAIL_USE_TLS'] = os.environ.get("MAIL_USE_TLS")

    mail.init_app(app)
from . import mongo
import re


def email_check(email):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return True
    else:
        return False


def user_check(username):
    if not (re.match(r'[a-zA-Z0-9\s]+$', username)):
        return False
    else:
        return True


def user_exist(email):
    user = mongo.db.users.find_one({"email": email})
    if user is None:
        return False
    else:
        return True


def task_assign_to(email):
    user = mongo.db.tasks.find_one({"email": email})
    if user is None:
        return False
    else:
        return True


def task_exist(email):
    user = mongo.db.tasks.find_one({"email": email})
    if user is None:
        return False
    else:
        return True

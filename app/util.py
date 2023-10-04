from . import mongo
import re
from flask import request
from json import dumps, loads
from marshmallow import ValidationError
from bson.objectid import ObjectId


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


def task_check(email):
    task = mongo.db.tasks.find_one({"email": email})
    if task is None:
        return False
    else:
        return True


def task_exit(task_id):
    try:
        task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    except Exception:
        return Exception("invalid object id")
    if task is None:
        return False
    else:
        return True


def role_valid(role):
    rolelist = ['ADMIN', 'MANAGER', 'EMPLOYEE']
    if role in rolelist:
        return False
    else:
        return True


def check_status(task):
    status_list = ["todo", "in-progress", "under-review", "done"]  
    if task['status'].casefold() not in status_list:
        msg = "enter a valid status"
        return msg
    return None


def data_now_json_str(schema):
    request_data = request.get_json()
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        raise err
    data_now_json_str = dumps(result)
    data = loads(data_now_json_str)
    return data
from . import mongo
import re
from flask import request, jsonify
from json import dumps, loads
from marshmallow import ValidationError


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


def data_now_json_str(schema):
    request_data = request.get_json()
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    data_now_json_str = dumps(result)
    data = loads(data_now_json_str)
   
    return data
from . import mongo
import re
from flask import request
from json import dumps, loads
from marshmallow import ValidationError
from bson.objectid import ObjectId
from flask_mail import Message
from app.config import sender_email
from app import mail


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
        return Exception("invalid object id"), 403
    if task is None:
        return False
    else:
        return True


def task_id_is_valid(task_id):
    try:
        task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
       
        if task is None:
            return None
        return True
    except Exception:
        return False


def role_valid(role):
    rolelist = ['admin', 'manager', 'employee']
    if role in rolelist:
        return False
    else:
        return True


def check_status(task):
    
    task = mongo.db.tasks.find_one({"_id": ObjectId(task['task_id'])})
    
    print("tt",task)
    status_list = ["todo", "in-progress", "under-review", "done"]
    if task['status'].lower() not in status_list:
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


def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc


def serialize_list(list):
    new_list = [serialize_doc(dictn) for dictn in list]
    return new_list


def mail_send(task_id, role, status):

    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    if status == "task_created":
        user = mongo.db.users.find_one({"_id": ObjectId(task['user_id'])})
        mail_body = "Hi , "+user['username'].capitalize() + "   your " + role.capitalize() + "  assign you a task  :- "+'"'+task['task_description'] + '"' 
        recipients_email = task['email']
    if status == "updated":
        if role == 'employee':
            user = mongo.db.users.find_one({"_id": ObjectId(task['assigned_by'])})
            mail_body = "Hi , " + user['username'].capitalize() + " status of " + '"' + task_id + '"' + " updated to " + '"' + task['status'] + '"'
            recipients_email = user['email']

        if role == "admin" or role == "manager":
            user = mongo.db.users.find_one({"_id": ObjectId(task['user_id'])})
            mail_body = "The status of your  task-id = " + '"' + task_id + '" ' + " , updated to  " + '"' + task['status'] + '"'
            recipients_email = task['email']
    print("mail", mail_body)
    print("recipients", recipients_email)
    msg = Message(
                         status,
                         sender=sender_email,
                         recipients=[recipients_email]
                                    )

    msg.body = mail_body
    mail.send(msg)


def calculate_salary(task_list):
    create = [None for li in task_list if li['status'] != 'done']
    print(create)
    if len(create) == 0:

        total_amount = [li['rate'] * li['time_needed'] for li in task_list]
        total_salary = sum(total_amount)
        print("total amou",total_amount)
        print("total_salary",total_salary)
        return total_salary
    
    return 0
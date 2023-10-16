from . import mongo
import re
from flask import request
from json import dumps, loads
from marshmallow import ValidationError
from bson.objectid import ObjectId
from app.helper_string import (salary_message, update_task_id,
                               update_status, assign_task, verification_mail,
                               confirmation_mail)
from app.token import token_decode
import base64 
from app.config import algorithum
from flask_mail import Message
from app.config import sender_email
from app import mail


def user_check(username):
    if not (re.match(r'[a-zA-Z0-9\s]+$', username)):
        return False
    else:
        return True


def task_details(field, data):
    task = mongo.db.tasks.find_one({field: data})
    return task


def user_details(field, data):
    user = mongo.db.users.find_one({field: data})
    return user


def user_exist(field, data):
    user = mongo.db.users.find_one({field: data})
    
    if user is None:
        return False
    else:
        return True


def get_supervisor(user):
    if user['role'] == 'employee':
        token = token_decode()
        if user['organization_name'] == token['organization_name']:
            return ObjectId(token['user_id'])
        return None
    if user['role'] == 'manager':
        admin_details = mongo.db.users.find_one({"organization_name": user['organization_name']})
        return admin_details['_id']
    return None


def task_exit(task_id):
    try:
        task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    except Exception:
        return Exception("invalid object id"), 403
    if task is None:
        return False
    else:
        return True


def orgnisation_exist(organization_name):
    orgnization = mongo.db.orgnizations.find_one({"organization_name": organization_name})
    if orgnization is None:
        return True
    return False


def task_id_is_valid(task_id):
    try:
        task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
        if task is None:
            return False
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


def mail_send(task_id, role, status, salary=0, payslip="not- generated"):
    if status == "salary":
        user = mongo.db.users.find_one({"_id": ObjectId(task_id)})
        mail_body = salary_message.format(user['username'].capitalize(),
                                          str(payslip), str(salary))
        recipients_email = user['email']
    if status == "verification":
        base64_string = encoded_string(task_id)
        recipients_email = task_id['email']
        link = "http://127.0.0.1:5000/admin/get_organisation/" + base64_string
        mail_body = verification_mail.format(link)

    if status == "confirmation":
        user = mongo.db.users.find_one({"_id": ObjectId(task_id)})
        recipients_email = user['email']
        mail_body = confirmation_mail.format(role)
    if status == "updated":
        task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
        if status == "task_created":
            user = mongo.db.users.find_one({"_id": ObjectId(task['user_id'])})
            mail_body = assign_task.format(user['username'].capitalize(), role.capitalize(),task['task_description'])
            recipients_email = task['email']
        if status == "updated":
            if role == 'employee':
                user = mongo.db.users.find_one({"_id": ObjectId(task['assigned_by'])})
                mail_body = update_status.format(user['username'].capitalize(), task_id, task['status']) 
                recipients_email = user['email']

            if role == "admin" or role == "manager":
                user = mongo.db.users.find_one({"_id": ObjectId(task['user_id'])})
                mail_body = update_task_id.format(task_id, task['status'])
                recipients_email = task['email']
    print("mail", mail_body)
    print("recipients", recipients_email)
    # msg = Message(
    #                      status,
    #                      sender=sender_email,
    #                      recipients=[recipients_email]
    #                                 )

    # msg.body = mail_body
    # mail.send(msg)


def calculate_salary(user_id, task_list):
    pay_slip = [" { " + str(li['rate']) + "$ " + " * " + str(li['time_needed'])+"hrs " + " => " + str(li['time_needed']*li['rate']) + " $" + "}" for li in task_list]
    user_id = "6524da755254ae7ce9b97f24"
    try:
        total_salary = mongo.db.tasks.aggregate([
          {"$match": {"user_id": user_id}},
          {"$group": {
            "_id": "$user_id",
            "total_sum": {
                "$sum": {
                    "$multiply": ["$time_needed", "$rate"]
                    }
                       }
                    }
                 }])
        total_salary = [x['total_sum'] for x in total_salary]

    except Exception as err:
        print("error",err)

    return (total_salary[0], pay_slip)


def encoded_string(user):
    data = user['email']+"," + user['organization_name']
    message_bytes = data.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_string = str(base64_bytes)
    base64_string = base64_string.split("b", 1)
    base64_string = base64_string[1]
    return base64_string


def decoded_string(token):
    decode_string = base64.b64decode(token)
    decode_string = decode_string.decode("utf-8")
    decode_string = decode_string.split(",")
    return decode_string
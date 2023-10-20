from . import mongo
import re
from flask import request
from json import dumps, loads
from marshmallow import ValidationError
from bson.objectid import ObjectId
from app.helper_string import (
    salary_message,
    update_task_id,
    update_status,
    assign_task,
    confirmation_mail,
    purposal_mail,
    verification_mail,
)
from app.token import token_decode
import base64
import random
from flask_mail import Message
from app.config import sender_email
from app import mail
import datetime
from app.config import algorithum
from flask_bcrypt import check_password_hash
import jwt


def user_check(username):
    if not (re.match(r"[a-zA-Z0-9\s]+$", username)):
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
    token = token_decode()
    return (token["user_id"], token["organization_name"])


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
    orgnization = mongo.db.orgnizations.find_one(
        {"organization_name": organization_name}
    )
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
    rolelist = ["admin", "manager", "employee"]
    if role in rolelist:
        return False
    else:
        return True


def check_status(task):
    status_list = ["todo", "in-progress", "under-review", "done"]
    if task["status"].lower() not in status_list:
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
        mail_body = salary_message.format(
            user["username"].capitalize(), str(payslip), str(salary)
        )
        recipients_email = user["email"]
    if status == "verification":
        base64_string, key = encoded_string(task_id)
        recipients_email = task_id["email"]
        link = "http://127.0.0.1:5000/admin/get_organisation/" + base64_string
        mail_body = link
    if status == "purposal":
        token = token_decode()
        print(task_id)
        print("tttt", task_id["organization_name"])
        company = mongo.db.orgnizations.find_one(
            {"organization_name": task_id["organization_name"]}
        )

        user = mongo.db.users.find_one({"_id": ObjectId(company["admin"])})
        recipients_email = user["email"]
        mail_body = purposal_mail.format(
            user["user_name"],
            user["organization_name"],
            task_id["task_description"],
            "www.google.com",
            "www.youtube.com",
        )
    if status == "confirmation":
        user = mongo.db.users.find_one({"_id": ObjectId(task_id)})
        recipients_email = user["email"]
        mail_body = confirmation_mail.format(role)
    if status == "updated":
        task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
        if status == "task_created":
            user = mongo.db.users.find_one({"_id": ObjectId(task["user_id"])})
            mail_body = assign_task.format(
                user["username"].capitalize(),
                role.capitalize(),
                task["task_description"],
            )
            recipients_email = task["email"]
        if status == "updated":
            if role == "employee":
                user = mongo.db.users.find_one({"_id": ObjectId(task["assigned_by"])})
                mail_body = update_status.format(
                    user["username"].capitalize(), task_id, task["status"]
                )
                recipients_email = user["email"]

            if role == "admin" or role == "manager":
                user = mongo.db.users.find_one({"_id": ObjectId(task["user_id"])})
                mail_body = update_task_id.format(task_id, task["status"])
                recipients_email = task["email"]
    print("mail", mail_body)
    print("recipients", recipients_email)
    msg = Message(status, sender=sender_email, recipients=[recipients_email])
    msg.body = mail_body
    if status == "verification":
        msg.html = verification_mail.format(link)
    if status == "purposal":
        msg.html = mail_body
    mail.send(msg)


def calculate_salary(user_id, task_list):
    pay_slip = [
        " { "
        + str(li["rate"])
        + "$ "
        + " * "
        + str(li["time_needed"])
        + "hrs "
        + " => "
        + str(li["time_needed"] * li["rate"])
        + " $"
        + "}"
        for li in task_list
    ]
    user_id = "6524da755254ae7ce9b97f24"
    try:
        total_salary = mongo.db.tasks.aggregate(
            [
                {"$match": {"user_id": user_id}},
                {
                    "$group": {
                        "_id": "$user_id",
                        "total_sum": {"$sum": {"$multiply": ["$time_needed", "$rate"]}},
                    }
                },
            ]
        )
        total_salary = [x["total_sum"] for x in total_salary]

    except Exception as err:
        print("error", err)

    return (total_salary[0], pay_slip)


def encoded_string(user):
    num = int(random.random() * 10000)
    data = user["email"] + "," + user["organization_name"] + "," + str(num)
    message_bytes = data.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_string = str(base64_bytes)
    base64_string = base64_string.split("b", 1)
    base64_string = base64_string[1]
    base64_string = base64_string.split("'")
    return base64_string[1], num


def decoded_string(token):
    decode_string = base64.b64decode(token)
    decode_string = str(decode_string)
    decode_string = decode_string.split("b", 1)
    decode_string = str(decode_string[1])
    decode_string = decode_string.split("'")
    decode_string = str(decode_string[1])
    return decode_string


def total_strength(organization_name):
    total_employee = list(
        mongo.db.users.aggregate(
            [
                {"$match": {"organization_name": organization_name}},
                {"$count": organization_name},
            ]
        )
    )
    for x in total_employee:
        return x[organization_name]


def technologies(organization_name):
    data = mongo.db.orgnizations.find_one({"organization_name": organization_name})
    return data["technology"]


def encoded_jwt(data):
    user = user_details("email", data["email"])
    if user is None:
        message = "There is no user, Please signup"
        return (message, False)
    try:
        if not check_password_hash(user["password"], data["password"]):
            message = "Please Enter the correct password"
            return (message, False)
    except Exception:
        message = "please update the details"
        return (message, False)

    if user["role"] != "client":
        payload = {
            "user_id": str(user["_id"]),
            "user_role": user["role"],
            "organization_name": str(user["organization_name"]),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=10),
        }
    else:
        payload = {
            "user_id": str(user["_id"]),
            "user_role": str(user["role"]),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=10),
        }

    encode_jwt = jwt.encode(payload, "secret", algorithm=algorithum)
    details = {"access token": str(encode_jwt), "user_id": str(user["_id"])}
    return (details, True)


def send_purposal(task):
    print("hiii", task)

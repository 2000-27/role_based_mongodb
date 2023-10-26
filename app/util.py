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
    accepted_mail,
    verification_mail,
    rejected_mail,
)
from app.token import token_decode
import base64
from flask_mail import Message
from app.config import sender_email
from app import mail
import datetime
from app.config import algorithum
from flask_bcrypt import check_password_hash
import math
from flask_paginate import get_page_parameter
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
        return task
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


def serialize_password(doc):
    doc["password"] = str(doc["password"])
    return doc


def serialize_list(list):
    new_list = [serialize_doc(dictn) for dictn in list]
    return new_list


def mail_send(user, role, status, salary=0, payslip="not- generated"):
    if status == "salary":
        user = mongo.db.users.find_one({"_id": ObjectId(user)})
        mail_body = salary_message.format(
            user["username"].capitalize(), str(payslip), str(salary)
        )
        recipients_email = user["email"]
    if status == "verification":
        base64_string = encoded_string(
            user["email"], user["organization_name"], user["user_name"]
        )
        recipients_email = user["email"]
        link = "http://127.0.0.1:5000/admin/get_organisation/" + base64_string

        mail_body = verification_mail.format(link)
    if status == "send_purposal":
        token = token_decode()
        company = mongo.db.orgnizations.find_one(
            {"organization_name": user["organization_name"]}
        )

        client = mongo.db.users.find_one({"_id": ObjectId(token["user_id"])})
        admin = mongo.db.users.find_one({"_id": ObjectId(company["admin"])})
        base64_string = encoded_string(client["email"], admin["email"])

        recipients_email = admin["email"]
        accept_link = "http://127.0.0.1:5000/admin/accept_purposal/" + base64_string
        reject_link = "http://127.0.0.1:5000/admin/reject_purposal/" + base64_string
        mail_body = purposal_mail.format(
            admin["user_name"],
            admin["organization_name"],
            user["task_description"],
            accept_link,
            reject_link,
        )

    if status == "accepted_purposal":
        client = user_details("email", user)
        admin = user_details("email", role)
        mail_body = accepted_mail.format(
            client["first_name"] + "  " + client["last_name"],
            admin["first_name"] + " " + admin["last_name"],
            admin["organization_name"],
        )
        recipients_email = client["email"]
    if status == "rejected_purposal":
        client = user_details("email", user)
        admin = user_details("email", role)
        mail_body = rejected_mail.format(
            client["first_name"] + "  " + client["last_name"],
            admin["first_name"] + " " + admin["last_name"],
            admin["organization_name"],
        )
        recipients_email = client["email"]
    if status == "confirmation":
        user = mongo.db.users.find_one({"_id": ObjectId(user)})
        recipients_email = user["email"]
        mail_body = confirmation_mail.format(role)

    if status == "task_created":
        task = mongo.db.tasks.find_one({"_id": user})
        user = mongo.db.users.find_one({"_id": ObjectId(task["user_id"])})
        mail_body = assign_task.format(
            user["user_name"].capitalize(),
            role.capitalize(),
            task["task_description"],
        )
        recipients_email = user["email"]

    # if status == "updated":
    #     if role == "employee":
    #         user = mongo.db.users.find_one({"_id": ObjectId(task["assigned_by"])})
    #         mail_body = update_status.format(
    #             user["username"].capitalize(), task_id, task["status"]
    #         )
    #         recipients_email = user["email"]

    #     if role == "admin" or role == "manager":
    #         user = mongo.db.users.find_one({"_id": ObjectId(task["user_id"])})
    #         mail_body = update_task_id.format(task_id, task["status"])
    #         recipients_email = task["email"]
    print("mail", mail_body)
    print("recipients", recipients_email)
    # msg = Message(status, sender=sender_email, recipients=[recipients_email])
    # msg.html = mail_body
    # mail.send(msg)


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


def encoded_string(
    email,
    organization_name,
    user_name="xxx",
):
    data = email + "," + organization_name + "," + user_name
    message_bytes = data.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_string = str(base64_bytes)
    base64_string = base64_string.split("b", 1)
    base64_string = base64_string[1]
    base64_string = base64_string.split("'")
    return base64_string[1]


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


def purposal(token, status):
    decoded_data = decoded_string(token)
    decoded_data = decoded_data.split(",")
    mail_send(decoded_data[0], decoded_data[1], status)


def view_all_employee():
    token = token_decode()
    admin = user_details("_id", ObjectId(token["user_id"]))
    manager = mongo.db.users.find({"supervisor": str(admin["_id"])})
    try:
        manager = [
            {
                "manager_Id": str(x["_id"]),
                "manager_Name": x["first_name"] + " " + x["last_name"],
                "manager_email": x["email"],
                "employee_details": [
                    {
                        "employee_Name": j["first_name"] + " " + j["last_name"],
                        "employee_email": j["email"],
                        "employee_ID": str(j["_id"]),
                    }
                    for j in list(mongo.db.users.find({"supervisor": str(x["_id"])}))
                ],
            }
            for x in list(mongo.db.users.find({"supervisor": str(admin["_id"])}))
        ]

        return manager
    except Exception as err:
        print(err)


def pagination(data):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 1
    offset = (page - 1) * per_page
    paginated_data = data[offset : offset + per_page]
    response = {
        "details": paginated_data,
        "page": page,
        "per_page": per_page,
        "total_record": len(data),
        "total_pages": math.ceil(len(data) / per_page),
        "sucess": True,
    }
    return response

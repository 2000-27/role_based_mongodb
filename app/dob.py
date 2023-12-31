from .util import (
    user_check,
    user_exist,
    task_id_is_valid,
    check_status,
    calculate_salary,
    get_supervisor,
    user_details,
    task_details,
    decoded_string,
    technologies,
    total_strength,
)
from . import mongo
from bson.objectid import ObjectId
from flask_bcrypt import generate_password_hash
from app.token import token_decode
from app.util import mail_send


def create_workspace(token):
    try:
        base64_string = decoded_string(token)
        base64_string = base64_string.split(",")
        data = mongo.db.orgnizations.find_one({"organization_name": base64_string[1]})
    except Exception as err:
        print("your error is ", err)
        data = None
    if data is None:
        user_id = mongo.db.users.insert_one(
            {
                "email": base64_string[0],
                "organization_name": base64_string[1],
                "role": "admin",
                "user_name": base64_string[2],
                "supervisor": "no",
            }
        ).inserted_id

        mongo.db.orgnizations.insert_one(
            {"organization_name": base64_string[1], "admin": str(user_id)}
        )
        print("organization is created successfully")
        message = "organization is created successfully"
        return message
    message = "organization is created successfully"
    return message


def update_workspace(user, token):
    try:
        base64_string = decoded_string(token)
        base64_string = base64_string.split(",")
        data = user_details("email", base64_string[0])
        if data is not None:
            real_password = user["password"]
            user_info = {
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "password": generate_password_hash(user["password"]),
                "pwd": user["password"],
            }
            filter = {"email": base64_string[0]}
            new_value = {"$set": user_info}
            mongo.db.users.update_one(filter, new_value)
            orgnisation_info = {
                "gst_number": user["gst_number"],
                "address": user["address"],
                "technology": user["technology"],
                "pincode": user["pincode"],
                "state": user["state"],
                "country": user["country"],
            }
            filter = {"organization_name": base64_string[1]}
            new_value = {"$set": orgnisation_info}
            mongo.db.orgnizations.update_one(filter, new_value)
            message = "updated sucessfully"
            return message
        message = "enter a valid url"
        return message

    except Exception:
        message = "Please enter a valid token"
        return message


def organisation_details(user):
    company = mongo.db.orgnizations.find_one(
        {"organization_name": user["organization_name"]}
    )
    if company is None:
        if user_exist("email", user["email"]):
            message = "This email is already register"
            return message
        if user_exist("user_name", user["user_name"]):
            message = "The username is already register"
            return message
        mail_send(user, "admin", "verification")
        message = "you get a verfication mail on your Email ID"
        return message
    message = "This organization is already register"
    return message


def add_user(user, role):
    if user_exist("email", user["email"]):
        message = "This email is already register"
        return message, False
    if user_exist("user_name", user["user_name"]):
        message = "This user_name is already register"
        return message, False
    if user["confirm_password"] != user["password"]:
        message = "Password and confirm password should be same"
        return message, False

    is_user_name_valid = user_check(user["user_name"])
    if is_user_name_valid is False:
        message = "Please enter a valid username"
        return message, False

    if role != "client":
        supervisor, organization_name = get_supervisor(user)
        mongo.db.users.insert_one(
            {
                "user_name": user["user_name"],
                "email": user["email"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "password": generate_password_hash(user["password"]),
                "role": role,
                "organization_name": organization_name,
                "supervisor": str(supervisor),
                "pwd": user["password"],
            }
        )
    else:
        mongo.db.users.insert_one(
            {
                "user_name": user["user_name"],
                "email": user["email"],
                "password": generate_password_hash(user["password"]),
                "role": role,
                "first_name": user["first_name"],
                "last_name": user["last_name"],
            }
        )

    message = "Register successfully"
    return message, True


def user_task(task, assign_by):
    try:
        decoded_jwt = token_decode()
        user_ids = [ObjectId(x) for x in task["user_id"]]
        user_info = list(
            mongo.db.users.find(
                {"_id": {"$in": user_ids}},
                {"supervisor": 1, "_id": 1},
            )
        )

        all_employee = list(
            mongo.db.users.find(
                {
                    "$and": [
                        {"supervisor": decoded_jwt["user_id"]},
                        {"_id": {"$in": user_ids}},
                    ]
                },
                {"supervisor": 1, "_id": 0},
            )
        )
        if len(task["user_id"]) != len(all_employee):
            message = "please enter a valid user_id"
            return message, False

        task_id = [
            {
                "user_id": str(user["_id"]),
                "assigned_by": decoded_jwt["user_id"],
                "task_description": task["task_description"],
                "status": "todo",
                "due_date": task["due_date"],
                "rate": task["rate"],
                "time_needed": 1,
            }
            for user in user_info
        ]
        mongo.db.tasks.insert_many(task_id)
        [mail_send(x, assign_by, "task_created") for x in task_id]
        message = "task is assigned"
        return message, True
    except Exception as err:
        print("your error is", err)
        message = "invalid user_id"
        return message, False


def task_delete(task):
    decoded_jwt = token_decode()
    if task_id_is_valid(task["task_id"]):
        task_info = task_details("_id", ObjectId(task["task_id"]))
        if task_info["assigned_by"] != decoded_jwt["user_id"]:
            message = "permission denied"
            return message, False
        mongo.db.tasks.delete_one({"_id": ObjectId(task["task_id"])})
        return message, True
    message = "Invalid objectId"
    return message, False


def update(task, updated_by):
    if task_id_is_valid(task["task_id"]):
        keysList = list(task.keys())
        if "status" in keysList:
            message = check_status(task)
            if message is not None:
                return message
        filter = {"_id": ObjectId(task["task_id"])}
        id = task.pop("task_id")
        new_value = {"$set": task}
        mongo.db.tasks.update_one(filter, new_value)
        if "status" in keysList:
            mail_send(id, updated_by, "updated")
        return True

    message = "Invalid objectId"
    return message


def salary_slip(user_id):
    complete_task_list = list(
        mongo.db.tasks.find({"user_id": user_id, "status": "done"})
    )
    all_task_list = list(task_details("user_id", user_id))
    if len(all_task_list) != len(complete_task_list):
        message = "All task are not completed"
        return message
    total_amount, payslip = calculate_salary(user_id, all_task_list)
    if total_amount:
        mail_send(user_id, "Employee", "salary", total_amount, payslip)
        message = "salary is generated"
        return message

    message = "All task are not completed"
    return message


def organization_info(all_organization_list):
    try:
        total_employee = [
            {
                "total_strength": total_strength(x),
                "organization_name": x,
                "technologies": technologies(x),
            }
            for x in all_organization_list
        ]

        return total_employee
    except Exception as err:
        print("your error is ", err)
        message = "please update all organization"
        return message

from .util import user_check, user_exist, task_exit, role_valid
from . import mongo
from bson.objectid import ObjectId
from flask_bcrypt import generate_password_hash


def add_user(user):
    if user_exist(user['email']):
        msg = "this email is already register"
        return msg
    if user['confirm_password'] != user['password']:
        msg = "Password and confirm password should be same"
        return msg
    is_user_name_valid = user_check(user['user_name'])
    if is_user_name_valid is False:
        msg = "Please enter a valid username"
        return msg
    if role_valid(user['role'].upper()):
        msg = "pls enter a valid role"
        return msg
    hash_password = generate_password_hash(user['password'])
    mongo.db.users.insert_one({
                "email": user['email'],
                "password": hash_password,
                "username": user['user_name'].upper(),
                "role": user['role'].upper(),
                }).inserted_id
    msg = "successfully register"
    return msg


def user_task(task, assign_by):
    if not user_exist(task['email']):
        msg = "user does not exist"
        return msg
    user = mongo.db.users.find_one({"email": task['email']})
    if user['role'] == "ADMIN":
        msg = "admin can assign task to manger and employee only"
        return msg
    mongo.db.tasks.insert_one({
                 "user_id": user['_id'],
                 "assigned_by": assign_by,
                 "email": task['email'],
                 "task_description": task['description'],
                 "status": "todo",
                 "due_date": task['due_date'],
                }).inserted_id
    msg = "task is assigned"
    return msg


def task_delete(task):
    try:
        if not user_exist(task['email']):
            msg = "user does not exist"
            return msg
        if not task_exit(task['task_id']):
            msg = "did't assign any task"
            return msg      
    except Exception as err:
        print("error",err)
        return Exception("invalid object id")

    mongo.db.tasks.delete_one({
        "_id": ObjectId(task['task_id'])
    })
    msg = "task is delete"
    return msg


def update(task):
    status_list = ["odo", "in-progress", "under-review", "done"]  
    if task['status'].casefold() not in status_list:
        msg = "enter a valid status"
        return msg
    filter = {'_id': ObjectId(task['task_id'])}
    keysList = list(task.keys())
    for field in keysList:
        if field != "task_id":
            data = {field: task[field]}
            update_field = {"$set": data}
            mongo.db.tasks.update_one(filter, update_field)
    msg = "task is update"
    return msg
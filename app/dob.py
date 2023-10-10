from .util import (user_check, user_exist,
                   task_id_is_valid, role_valid, check_status)
from . import mongo
from bson.objectid import ObjectId
from flask_bcrypt import generate_password_hash
from app.token import token_decode
from app.util import mail_send


def add_user(user):
    if user_exist(user['email']):
        message = "This email is already register"
        return message
    if user['confirm_password'] != user['password']:
        message = "Password and confirm password should be same"
        return message
    is_user_name_valid = user_check(user['user_name'])
    if is_user_name_valid is False:
        message = "Please enter a valid username"
        return message
    if role_valid(user['role']):
        message = "Please enter a valid role"
        return message
    hash_password = generate_password_hash(user['password'])
    mongo.db.users.insert_one({
                "email": user['email'],
                "password": hash_password,
                "username": user['user_name'],
                "role": user['role'],
                }).inserted_id
    message = True
    return message


def user_task(task, assign_by):
    if not user_exist(task['email']):
        message = "user does not exist"
        return message
    user = mongo.db.users.find_one({"email": task['email']})
    if user['role'] == "ADMIN":
        message = "admin can assign task to manger and employee only"
        return message
    decoded_jwt = token_decode()
    if ObjectId(decoded_jwt['user_id']) == user['_id']:
        message = "permission denied"
        return message
    print("ddfsdf",task)
    task_id = mongo.db.tasks.insert_one({
                 "user_id": str(user['_id']),
                 "assigned_by": decoded_jwt['user_id'],
                 "email": task['email'],
                 "task_description": task['description'],
                 "status": "todo",
                 "due_date": task['due_date'],
                 "rate": task['rate'],
                 "time_needed": 0
                }).inserted_id
    mail_send(task_id, assign_by, "task_created")
    message = True
    return message


def task_delete(task):

    if task_id_is_valid(task['task_id']) is None:
        message = "Invalid ObjectId"
        return message
   
    if task_id_is_valid(task['task_id']):
        mongo.db.tasks.delete_one({
            "_id": ObjectId(task['task_id'])
        })
        message = True
        return message

    message = "Invalid objectId"
    return message


def update(task, updated_by):
    
    task_id_valid = task_id_is_valid(task['task_id'])   
    if task_id_valid is None:
        
        raise Exception("invalid ObjectId")

    keysList = list(task.keys())
    if 'status' in keysList:
        message = check_status(task)
        if message is not None:
            return message

    if task_id_valid:
        filter = {'_id': ObjectId(task['task_id'])}
        keysList = list(task.keys())
        for field in keysList:
            if field != "task_id":
                data = {field: task[field]}
                update_field = {"$set": data}

                mongo.db.tasks.update_one(filter, update_field)
        message = True
        mail_send(task['task_id'], updated_by, "updated")
        return message

    message = "Invalid objectId"
    return message

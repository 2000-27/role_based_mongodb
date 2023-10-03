from .util import user_check, user_exist, task_check
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
    hash_password = generate_password_hash(user['password'])
    mongo.db.users.insert_one({
                "email": user['email'],
                "password": hash_password,
                "username": user['user_name'],
                "role": user['role'],
                }).inserted_id
    msg = "successfully register"
    return msg


def user_task(task, assign_by):
    if not user_exist(task['email']):
        msg = "user does not exist"
        return msg
    user = mongo.db.users.find_one({"email": task['email']})
    
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
    if not task_check(task['email']):
        msg = "did't assign any task"
        return msg
    mongo.db.tasks.delete_one({
        "email": task['email']
    })
    msg = "task is delete"
    return msg


def update(task):
    filter = {'_id': ObjectId(task['task_id'])}
    keysList = list(task.keys())
    print("mykeylist is ", keysList)

    if 'new_task' in keysList:
        new_task = {"$set": {'task_description': task['new_task']}}  
        mongo.db.tasks.update_one(filter, new_task)
    
    if 'status' in keysList:
        new_status = {"$set": {'status': task['status']}}
        mongo.db.tasks.update_one(filter, new_status)
    if 'email' in keysList:
        new_status = {"$set": {'email': task['email']}}
        mongo.db.tasks.update_one(filter, new_status)

    msg = "task is update"
    return msg
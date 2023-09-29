from .util import user_check, user_exist, task_check
from . import mongo


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
    mongo.db.users.insert_one({
                "email": user['email'],
                "password": user['password'],
                "username": user['user_name'],
                "role": user['role'],
                }).inserted_id
    msg = "successfully register"
    return msg


def user_task(task, assign_by):
    if not user_exist(task['email']):
        msg = "user does not exist"
        return msg
    if task_check(task['email']):
        msg = "task is already assign"
        return msg
    mongo.db.tasks.insert_one({
                "assigned_by": assign_by,
                "email": task['email'],
                "task": task['task'],
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
    if not task_check(task['email']):
        msg = "did't assign any task"
        return msg
    filter = {'email': task['email']}
    newvalues = {"$set": {'task': task['task']}}
    mongo.db.tasks.update_one(filter, newvalues)
    msg = "task is update"
    return msg
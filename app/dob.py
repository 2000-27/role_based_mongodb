from .util import (email_check, user_check,
                   user_exist, task_assign_to, task_exist)
from . import mongo


def add_user(user):
    is_user_name_valid = user_check(user['user_name'])
    if user_exist(user['email']):
        msg = "this email is already register"
        return msg
    if user['confirm_password'] != user['password']:
        msg = "Password and confirm password should be same"
        return msg
    if email_check(user['email']):
        msg = "Please enter a valid email address"
        return msg
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


def user_task(task):
    if email_check(task['email']):
        msg = "Please enter a valid email address"
        return msg
    if not user_exist(task['email']):
        msg = "user does not exit"
        return msg
    if task_assign_to(task['email']):
        msg = "task is already assign"
        return msg
    mongo.db.tasks.insert_one({
                "assigned_by": "ADMIN",
                "email": task['email'],
                "password": task['task'],
                "username": task['due_date'],
                }).inserted_id
    msg = "task assigned"
    return msg


def task_delete(task):
    if not task_exist(task['email']):
        msg = "task does not exit"
        return msg
    mongo.db.tasks.delete_one({
        "email": task['email']
    })
    msg = "task is delete"
    return msg


def task_update(task):
    if not task_exist(task['email']):
        msg = "task does not exit"
        return msg  
    mongo.db.tasks.update_one(
        {"email": task['email']},

        {set: {"task": "new task"}})
    msg = "task is update"
    return msg

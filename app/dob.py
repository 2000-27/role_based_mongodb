from .util import (user_check, user_exist,
                   task_id_is_valid, role_valid,
                   check_status, calculate_salary, orgnisation_exist,
                   get_supervisor, user_details, task_details, decoded_string)
from . import mongo
from bson.objectid import ObjectId
from flask_bcrypt import generate_password_hash
from app.token import token_decode
import copy
from app.util import mail_send


def create_workspace(token):
    try:
        base64_string = decoded_string(token)
        base64_string = base64_string.split(",")
        data = mongo.db.orgnizations.find_one({"organization_name": base64_string[1]})
    except Exception:
        data = None
    if data is None:
        user_id = mongo.db.users.insert_one({
                "email": base64_string[0],
                "organization_name": base64_string[1],
                "role": "admin",
                'supervisor': "no"
            }).inserted_id

        mongo.db.orgnizations.insert_one({
                "organization_name": base64_string[1],
                "admin": str(user_id)
            })
        message = "organization is created successfully"

    message = "organization is already created"
    return message    


def update_workspace(user, token):
    try:
        base64_string = decoded_string(token)
        base64_string = base64_string.split(",")
        data = mongo.db.users.find_one({"email": base64_string[0]})
        if data is not None:
            real_password = user['password']
            hash_password = generate_password_hash(user['password'])
            user_info = {
                "user_name": user['user_name'],
                "password": hash_password
            }
            filter = {'email': base64_string[0]}
            new_value = {"$set": user_info}
            mongo.db.users.update_one(filter, new_value)
            orgnisation_info = {
                "gst_number": user['gst_number'],
                "address": user['address'],
                "pincode": user['pincode'],
                "state": user['state'],
                'country': user['country'] 
            }
            filter = {'organization_name': base64_string[1]}
            new_value = {"$set": orgnisation_info}
            mongo.db.orgnizations.update_one(filter, new_value)
            message = "updated sucessfully"
            return message
        message = "your organization is not created"
        return message
    
    except Exception:
        message = "Please enter a valid token"
        return message


def organisation_details(user):
    company = mongo.db.orgnizations.find_one({"organization_name": user['organization_name']})
    if company is None:
        if user_exist("email", user['email']):
            message = "This email is already register"
            return message
        mail_send(user, "admin", "verification")
        message = "you get a verfication mail on your Email ID"
        return message
    message = "This organization is already register"
    return message


def add_user(user):
    if user_exist("email", user['email']):
        message = "This email is already register"
        return message
    if user['confirm_password'] != user['password']:
        message = "Password and confirm password should be same"
        return message

    if orgnisation_exist(user['organization_name']):
        message = "Please enter a valid company_name"
        return message

    supervisor = get_supervisor(user)
    if supervisor is None:
        message = "Please enter the same orgnization name"
        return message
    is_user_name_valid = user_check(user['user_name'])
    if is_user_name_valid is False:
        message = "Please enter a valid username"
        return message
    if role_valid(user['role']):
        message = "Please enter a valid role"
        return message

    hash_password = generate_password_hash(user['password'])
    user['password'] = hash_password
    user['confirm_password'] = hash_password
  
    mongo.db.users.insert_one({
        "user_name": user['user_name'],
        "email": user['email'],
        "password": user['password'],
        "role": user['role'],
        "organization_name": user['organization_name'],
        'supervisor': str(supervisor)
    })

    message = "Register successfully"
    return message


def user_task(task, assign_by):

    if not user_exist("_id", ObjectId(task['user_id'])):
        message = "user does not exist"
        return message
    
    user = user_details("_id", ObjectId(task['user_id']))
    if user['role'] == "ADMIN":
        message = "admin can assign task to manger only"
        return message
    
    decoded_jwt = token_decode()
    if ObjectId(decoded_jwt['user_id']) == user['_id']:
        message = "permission denied"
        return message

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
    if task_id_is_valid(task['task_id']):
        mongo.db.tasks.delete_one({
            "_id": ObjectId(task['task_id'])
        })
        return True

    message = "Invalid objectId"
    return message


def update(task, updated_by):
    if task_id_is_valid(task['task_id']):
        keysList = list(task.keys())
        if 'status' in keysList:
            message = check_status(task)
            if message is not None:
                return message

        temp_dict = copy.deepcopy(task)
        del temp_dict['task_id']
        filter = {'_id': ObjectId(task['task_id'])}
        new_value = {"$set": temp_dict}
        mongo.db.tasks.update_one(filter, new_value)

        if 'status' in keysList:
            mail_send(task['task_id'], updated_by, "updated")
        return True

    message = "Invalid objectId"
    return message


def salary_slip(user_id):
    complete_task_list = list(mongo.db.tasks.find({'user_id': user_id,
                                                    "status": "done"}))
    all_task_list = list(task_details('user_id', user_id))
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


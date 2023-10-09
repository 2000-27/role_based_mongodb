from flask import jsonify, Blueprint, request
from app.token import manager_required
from . import mongo
from app.token import token_decode
from app.dob import add_user, user_task, task_delete, update
from app.util import serialize_list, serialize_doc
from app.util import data_now_json_str, calculate_salary
from app.schema import TaskSchema, UserSchema, InfoSchema, UpdateSchema
from bson.objectid import ObjectId
manager_bp = Blueprint("manager", __name__, url_prefix="manager")


@manager_bp.route('/create-user', endpoint='create_user', methods=['POST'])
@manager_required
def create_user():
    message = ""
    user_schema = UserSchema()
    try:
        user = data_now_json_str(user_schema)
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400

    if user['role'] != "manager":
        message = add_user(user)
        if message is True:
            return jsonify({"success": True, "message": "Register sucessfully"
                            }), 200
        return jsonify({"success": True, "message": message}), 400
    message = "Manager can add only employee"
    return jsonify({"success": False, "message": message}), 400


@manager_bp.route('/view-task', endpoint='view_task', methods=['GET'])
@manager_required
def view_task():
    task_id = request.args.get('task_id', default=None)
    decoded_jwt = token_decode()
    user_id = decoded_jwt['user_id']
    if task_id is None:
        all_task = list(mongo.db.tasks.find({'assigned_by': user_id}))

        if len(all_task) == 0:
            return jsonify({"success": False, "message":
                            "No task is assign"}), 400
        all_task = serialize_list(all_task)
        return jsonify({"success": True, "details": all_task}), 200

    try:
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if user_id == task['assigned_by']:
            task = serialize_doc(task)
            return jsonify({"success": True, "details": task})
        return jsonify({"success": False, "message": ""})
    except Exception:
        return jsonify({"success": False, "message": "invalid ObjectId"}), 400


@manager_bp.route('/create-task', endpoint='create_task', methods=['POST'])
@manager_required
def create_task():
    task_schema = TaskSchema()
    try:
        user = data_now_json_str(task_schema)
        message = user_task(user, "manager")
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 401
    if message is True:
        return jsonify({"success": True, "message": "Task is assigned"
                        }), 200
    return jsonify({"success": False, "message": message}), 400


@manager_bp.route('/delete-task', endpoint='delete-task', methods=['DELETE'])
@manager_required
def delete_task():
    message = ""
    info_schema = InfoSchema()
    try:
        task = data_now_json_str(info_schema)
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 401

    try:
        token = token_decode()
        task_details = mongo.db.tasks.find_one({"_id":
                                                ObjectId(task['task_id'])})
        if token['user_id'] == task_details['assigned_by']:
            message = task_delete(task)
            if message is True:
                return jsonify({"success": True, "message":
                                "task is deleted"}), 200
            return jsonify({"success": False, "message": message}), 400
        return jsonify({"success": False, "message": "Permission denied"}), 401
    except Exception as err:
        return jsonify({"success": False, "message":"invalid objectId"}), 400


@manager_bp.route('/update-task', endpoint='update_task', methods=['POST'])
@manager_required
def update_task():
    message = ""
    update_schema = UpdateSchema()
    try:
        task = data_now_json_str(update_schema)
        token = token_decode()
        task_details = mongo.db.tasks.find_one({"_id":
                                                ObjectId(task['task_id'])})
        if token['user_id'] == task_details['assigned_by']:
            message = update(task, "manager")
            if message is True:
                return jsonify({"success": True, "message": "task is updated"}), 200
            return jsonify({"success": False, "message": message}), 400
        return jsonify({"success": False, "message": "Permission denied"}), 401
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400


@manager_bp.route('/generate-salary', endpoint='assign_salary',
                  methods=['GET'])
@manager_required
def assign_salary():
    user_id = request.args.get('user_id', default=None)
    if user_id is not None:
        try:
            all_task_list = list(mongo.db.tasks.find({'user_id': user_id}))
            print("allll ",len(all_task_list))
            totol_amount =  calculate_salary(all_task_list)
            if totol_amount != 0:
                return jsonify({"success": True,
                                "Your Salary is (in $) ": totol_amount}), 200
            return jsonify({"success": False,
                            "message ": "Please complete your all task"}), 200
            
        except Exception:
            message = "Invalid ObjectId"
            return jsonify({"success": False, "message": message}), 400

    return jsonify({"success": False, "message": "Please Enter a user id " }), 400 
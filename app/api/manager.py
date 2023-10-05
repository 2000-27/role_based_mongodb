from flask import jsonify, Blueprint, request
from app.token import manager_required
from . import mongo
from app.token import token_decode
from app.dob import add_user, user_task, task_delete, update
from app.util import data_now_json_str
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
        return jsonify({"success": True, "message": message}), 403
    message = "Manager can add only employee"
    return jsonify({"success": False, "message": message}), 403


@manager_bp.route('/view-task', endpoint='view_task',  methods=['GET'])
@manager_required
def view_task():
    task_id = request.args.get('task_id', default=None)
    decoded_jwt = token_decode()
    user_id = decoded_jwt['user_id']
    if task_id is None:
        all_task = list(mongo.db.tasks.find({'assigned_by': user_id}))
        if all_task is None:
            return jsonify({"success": False, "message": "No task is assign"}), 403
        return jsonify({"success": True, "message": str(all_task)}), 200

    try:
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        if user_id == task['assigned_by']:
            return jsonify({"success": True, "message": str(task)})
        return jsonify({"success": False, "message": ""})
    except Exception:
        return jsonify({"success": False, "message": "invalid task id"}), 403



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
    return jsonify({"success": False, "message": message}), 403


@manager_bp.route('/delete-task', endpoint='delete-task', methods=['DELETE'])
@manager_required
def delete_task():
    message = ""
    info_schema = InfoSchema()
    try:
        task = data_now_json_str(info_schema)
        token = token_decode()
        task_details = mongo.db.tasks.find_one({"_id":ObjectId(task['task_id'])})
        if token['user_id']==task_details['assigned_by']:
            message = task_delete(task)
                
            if message is True:
                return jsonify({"success": True, "message": "task is deleted"}), 200
            return jsonify({"success": False, "message": message}), 403
        return jsonify({"success": False, "message": "permission denied"}), 401
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400


@manager_bp.route('/update-task', endpoint='update_task', methods=['POST'])
@manager_required
def update_task():
    message = ""
    update_schema = UpdateSchema()
    try:
        task = data_now_json_str(update_schema)
        token = token_decode()
        task_details = mongo.db.tasks.find_one({"_id": ObjectId(task['task_id'])})
        if token['user_id'] == task_details['assigned_by']:
            message = update(task)
         
            if message is True:
                return jsonify({"success": True, "message": "task is updated"}), 200
            return jsonify({"success": False, "message": message}), 403
        return jsonify({"success": False, "message": "permission denied"}), 401
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400

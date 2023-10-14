from flask import jsonify, Blueprint, request
from app.token import employee_required
from app.schema import StatusSchema
from app.token import token_decode
from app.util import (data_now_json_str, serialize_doc, serialize_list,
                      task_id_is_valid)
from app.dob import update
from bson.objectid import ObjectId
from app import mongo
employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


@employee_bp.route('/view-task', endpoint='view_task',  methods=['GET'])
@employee_required
def view_task():
    task_id = request.args.get('task_id', default=None)
    if task_id is not None:
        task = task_id_is_valid(task_id)
        if task_id_is_valid(task_id):
            try:
                task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
                task = serialize_doc(task)
                return jsonify({"success": True, "details": task}), 200
            except Exception as err:
                return jsonify({"success": True, "details": str(err)}), 200
        return jsonify({"success": False, "message": "Invalid ObjectId"}), 200

    decoded_jwt = token_decode()
    user = mongo.db.users.find_one({'_id': ObjectId(decoded_jwt['user_id'])})
    all_task_list = list(mongo.db.tasks.find({'email': user['email']}))
    if not len(all_task_list):
        
        return jsonify({"success": False, "message":
                        "No task is assign"}), 400

    all_task_list = serialize_list(all_task_list)
    return jsonify({"success": True, "details": all_task_list}), 200


@employee_bp.route('/status-change', endpoint='change_status',
                   methods=['PATCH'])
@employee_required
def change_status():
    message = ""
    status_schema = StatusSchema()
    try:
        task = data_now_json_str(status_schema)
        message = update(task, "employee")
        if message is True:
            return jsonify({"success": True,
                            "message": "status is updated"}), 200
        return jsonify({"success": False, "message": message}), 400
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400

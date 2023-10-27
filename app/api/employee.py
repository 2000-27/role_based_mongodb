from flask import jsonify, Blueprint, request
from app.token import employee_required
from app.schema import StatusSchema
from app.token import token_decode
from app.util import (
    data_now_json_str,
    serialize_doc,
    serialize_list,
    pagination,
    user_details,
    task_details,
)
from app.dob import update
from bson.objectid import ObjectId
from app import mongo

employee_bp = Blueprint("employee", __name__, url_prefix="/employee")


@employee_bp.route("/view-task", endpoint="view_task", methods=["GET"])
@employee_required
def view_task():
    decoded_jwt = token_decode()
    task_id = request.args.get("task_id", default=None)
    if task_id is not None:
        try:
            task = task_details("_id", ObjectId(task_id))
            print(task)
            if task["user_id"] == decoded_jwt["user_id"]:
                task = serialize_doc(task)
                return jsonify({"success": True, "details": task}), 200
            return jsonify({"success": False, "details": "There is no such task"}), 400
        except Exception as err:
            print(err)
            return jsonify({"success": False, "details": "invalid task Id"}), 400

    user = user_details("_id", ObjectId(decoded_jwt["user_id"]))
    all_task_list = list(mongo.db.tasks.find({"user_id": str(user["_id"])}))
    all_task_list = serialize_list(all_task_list)
    if not len(all_task_list):
        return jsonify({"success": False, "message": "No task is assign"}), 400
    response = pagination(all_task_list)
    return jsonify(response)


@employee_bp.route("/status-change", endpoint="change_status", methods=["PATCH"])
@employee_required
def change_status():
    status_schema = StatusSchema()
    try:
        task = data_now_json_str(status_schema)
        message, response = update(task, "employee")
        if response:
            return jsonify({"success": True, "message": "status is updated"}), 200
        return jsonify({"success": False, "message": message}), 400
    except Exception as err:
        print("your err is", err)
        return jsonify({"success": False, "message": str(err)}), 400

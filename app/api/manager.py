from flask import jsonify, Blueprint, request
from app.token import manager_required
from app.token import token_decode
from app.dob import add_user, user_task, task_delete, update, salary_slip
from app.util import (
    serialize_doc,
    data_now_json_str,
    task_details,
)
from app.schema import TaskSchema, UserSchema, InfoSchema, UpdateSchema, StatusSchema
from bson.objectid import ObjectId

manager_bp = Blueprint("manager", __name__, url_prefix="manager")


@manager_bp.route("/create-user", endpoint="create_user", methods=["POST"])
@manager_required
def create_user():
    message = ""
    user_schema = UserSchema()
    try:
        user = data_now_json_str(user_schema)
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400
    message, response = add_user(user, "employee")
    if response:
        return jsonify({"success": True, "message": message}), 200
    return jsonify({"success": True, "message": message}), 400


@manager_bp.route("/view-task", endpoint="view_task", methods=["GET"])
@manager_required
def view_task():
    task_id = request.args.get("task_id", default=None)
    decoded_jwt = token_decode()
    user_id = decoded_jwt["user_id"]
    if task_id is None:
        all_task = task_details("assigned_by", user_id)
        if len(all_task) == 0:
            return jsonify({"success": False, "message": "No task is assign"}), 400
        all_task = serialize_doc(all_task)
        return jsonify({"success": True, "details": all_task}), 200

    try:
        task = task_details("assigned_by", user_id)
        task = serialize_doc(task)
        return jsonify({"success": True, "details": task})
    except Exception:
        return jsonify({"success": False, "message": "invalid ObjectId"}), 400


@manager_bp.route("/create-task", endpoint="create_task", methods=["POST"])
@manager_required
def create_task():
    task_schema = TaskSchema()
    try:
        user = data_now_json_str(task_schema)
        message, response = user_task(user, "manager")
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400
    if response:
        return jsonify({"success": True, "message": "Task is assigned"}), 200
    return jsonify({"success": False, "message": message}), 400


@manager_bp.route("/delete-task", endpoint="delete-task", methods=["DELETE"])
@manager_required
def delete_task():
    message = ""
    info_schema = InfoSchema()
    try:
        task = data_now_json_str(info_schema)
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400

    try:
        message, response = task_delete(task)
        if response:
            return jsonify({"success": True, "message": "task is deleted"}), 200
        return jsonify({"success": False, "message": message}), 400
    except Exception:
        return jsonify({"success": False, "message": "invalid objectId"}), 400


@manager_bp.route("/update-task", endpoint="update_task", methods=["PATCH"])
@manager_required
def update_task():
    update_schema = UpdateSchema()
    try:
        task = data_now_json_str(update_schema)
        message, response = update(task, "manager")
        if response:
            return jsonify({"success": True, "message": "task is updated"}), 200
        return jsonify({"success": False, "message": message}), 400

    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400


@manager_bp.route("/generate-salary", endpoint="assign_salary", methods=["PATCH"])
@manager_required
def assign_salary():
    user_id = request.args.get("user_id", default=None)
    if user_id is not None:
        try:
            task = task_details("user_id", user_id)
            if task is not None:
                message = salary_slip(user_id)
                print("salaryyyy", message)
                return jsonify({"success": False, "message": message}), 400
            message = "Invalid ObjectId"
            return jsonify({"success": False, "message": message}), 400
        except Exception as err:
            message = "Invalid ObjectId"
            return jsonify({"success": False, "message": str(err)}), 400

    return jsonify({"success": False, "message": "Please enter valid a user id"}), 400

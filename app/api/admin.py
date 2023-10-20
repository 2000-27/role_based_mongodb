from flask import jsonify, Blueprint
from app.token import admin_required
from app.dob import (
    add_user,
    user_task,
    task_delete,
    update,
    update_workspace,
    organisation_details,
    create_workspace,
)
from app.schema import (
    TaskSchema,
    InfoSchema,
    UserSchema,
    UpdateSchema,
    OrgnizationSchema,
    getInfoSchema,
)
from app.util import data_now_json_str

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route(
    "/get_organisation/<token>", endpoint="get_organisation", methods=["GET"]
)
def get_organisation(token):
    try:
        message = create_workspace(token)
        return jsonify({"success": True, "message": message}), 400
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400


@admin_bp.route(
    "/update_organization/<token>", endpoint="update_organization", methods=["POST"]
)
def update_organization(token):
    try:
        orgnization_schema = OrgnizationSchema()
        data = data_now_json_str(orgnization_schema)
        message = update_workspace(data, token)
        return jsonify({"success": True, "message": message}), 200
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400


@admin_bp.route("/create_orgnization", endpoint="create_orgnization", methods=["POST"])
def create_orgnization():
    info_schema = getInfoSchema()
    try:
        data = data_now_json_str(info_schema)
        message = organisation_details(data)
        return jsonify({"success": True, "message": message}), 200
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400


@admin_bp.route("/create-user", endpoint="create_user", methods=["POST"])
@admin_required
def create_user():
    message = ""
    user_schema = UserSchema()
    try:
        user = data_now_json_str(user_schema)
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400
    message, response = add_user(user, "manager")
    if response:
        return jsonify({"success": True, "message": message}), 200
    return jsonify({"success": True, "message": message}), 400


@admin_bp.route("/create-task", endpoint="create_task", methods=["POST"])
@admin_required
def create_task():
    message = ""
    task_schema = TaskSchema()
    try:
        user = data_now_json_str(task_schema)
        message = user_task(user, "admin")
    except Exception as err:
        return jsonify({"success": False, "mesage": str(err)}), 401
    if message is True:
        return jsonify({"success": True, "message": "Task is assigned"}), 200

    return jsonify({"success": False, "message": message}), 400


@admin_bp.route("/delete-task", endpoint="delete-task", methods=["DELETE"])
@admin_required
def delete_task():
    info_schema = InfoSchema()
    try:
        task_id = data_now_json_str(info_schema)
        message = task_delete(task_id)
        if message is True:
            return jsonify({"success": True, "message": "task is deleted"}), 200
        return jsonify({"success": False, "message": message}), 400
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400


@admin_bp.route("/update-task", endpoint="update-task", methods=["PATCH"])
@admin_required
def update_task():
    message = ""
    update_schema = UpdateSchema()
    try:
        task_id = data_now_json_str(update_schema)
        message = update(task_id, "admin")
        if message is True:
            return jsonify({"success": True, "message": "task is updated "}), 200
        return jsonify({"success": False, "message": message}), 400
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400

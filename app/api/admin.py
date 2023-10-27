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
from app.util import (
    data_now_json_str,
    purposal,
    view_all_employee,
    pagination,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route(
    "/get_organisation/<token>", endpoint="get_organisation", methods=["GET"]
)
def get_organisation(token):
    try:
        message = create_workspace(token)
        return jsonify({"success": True, "message": message}), 200
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


@admin_bp.route("/accept_purposal/<token>", endpoint="accept_purposal", methods=["GET"])
def accept_purposal(token):
    purposal(token, "accepted_purposal")
    return jsonify({"success": True, "message": "purposal is accepted"})


@admin_bp.route("/reject_purposal/<token>", endpoint="reject_purposal", methods=["GET"])
def reject_purposal(token):
    purposal(token, "rejected_purposal")
    return jsonify({"success": True, "message": "purposal is rejected"})


@admin_bp.route("/create-user", endpoint="create_user", methods=["POST"])
@admin_required
def create_user():
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
    task_schema = TaskSchema()
    try:
        task = data_now_json_str(task_schema)
        message, response = user_task(task, "admin")
    except Exception as err:
        return jsonify({"success": False, "mesage": str(err)}), 400
    if response:
        return jsonify({"success": True, "message": message}), 200
    return jsonify({"success": False, "message": message}), 400


@admin_bp.route("/delete-task", endpoint="delete-task", methods=["DELETE"])
@admin_required
def delete_task():
    info_schema = InfoSchema()
    try:
        task_id = data_now_json_str(info_schema)
        message, response = task_delete(task_id)
        if response:
            return jsonify({"success": True, "message": "task is deleted"}), 200
        return jsonify({"success": False, "message": message}), 400
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400


@admin_bp.route("/update-task", endpoint="update-task", methods=["PATCH"])
@admin_required
def update_task():
    update_schema = UpdateSchema()
    try:
        updated_record = data_now_json_str(update_schema)
        message, response = update(updated_record, "admin")
        if response:
            return jsonify({"success": True, "message": message}), 200
        return jsonify({"success": False, "message": message}), 400
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400


@admin_bp.route("/view_employee", endpoint="view_employee", methods=["GET"])
@admin_required
def view_employee():
    try:
        data = view_all_employee()
        response = pagination(data)
        return jsonify(response), 200
    except Exception as err:
        return jsonify(str(err)), 400

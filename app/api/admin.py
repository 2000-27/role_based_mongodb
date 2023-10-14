from flask import jsonify, Blueprint, request
from app.token import admin_required
from app.dob import (add_user, user_task, task_delete, update, orgnization)
from app.schema import (TaskSchema, InfoSchema,
                        UserSchema, UpdateSchema, OrgnizationSchema)
from app.util import data_now_json_str, role_valid
from app.config import Organisation_key
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/create_orgnization', endpoint='create_orgnization',
                methods=['POST', 'PATCH'])
def create_orgnization():
    orgnization_key = request.args.get('organization_key', default=None)
    if orgnization_key is None:
        message = "organization_key required"
        return jsonify({"success": False, "message": message}), 400  
    
    if orgnization_key == Organisation_key:
        orgnization_schema = OrgnizationSchema()
        try:
            data = data_now_json_str(orgnization_schema)
            message = orgnization(data)
            return jsonify({"success": True, "message": message}), 200
        except Exception as err:
            return jsonify({"success": False, "message": str(err)}), 400
    message = "invalid organization key"
    return jsonify({"success": False, "message": message}), 400    


@admin_bp.route('/create-user', endpoint='create_user', methods=['POST'])
@admin_required
def create_user():    
    message = ""
    user_schema = UserSchema()
    try:
        user = data_now_json_str(user_schema)
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400
    if role_valid(user['role']):
        message = "Enter a valid role"
        return jsonify({"success": False, "message": message}), 400

    if user['role'] == "manager":
        message = add_user(user)
        if message is True:
            return jsonify({"success": True, "message": "Register sucessfully"
                            }), 200
        return jsonify({"success": True, "message": message}), 400
    message = "Admin can add only manager"
    return jsonify({"success": False, "message": message}), 400


@admin_bp.route('/create-task', endpoint='create_task', methods=['POST'])
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
        return jsonify({"success": True, "message": "Task is assigned"
                        }), 200

    return jsonify({"success": False, "message": message}), 400


@admin_bp.route('/delete-task', endpoint='delete-task', methods=['DELETE'])
@admin_required
def delete_task():
    info_schema = InfoSchema()
    try:
        task_id = data_now_json_str(info_schema)
        message = task_delete(task_id)
        if message is True:
            return jsonify({"success": True, "message":
                            "task is deleted"}), 200
        return jsonify({"success": False, "message": message}), 400
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400


@admin_bp.route('/update-task', endpoint='update-task', methods=['PATCH'])
@admin_required
def update_task():
    message = ""
    update_schema = UpdateSchema()
    try:
        task_id = data_now_json_str(update_schema)     
        message = update(task_id, "admin")
        if message is True:
            return jsonify({"success": True, "message":
                            "task is updated "}), 200
        return jsonify({"success": False, "message": message}), 400
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400

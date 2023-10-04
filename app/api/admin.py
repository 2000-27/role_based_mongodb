from flask import jsonify, Blueprint
from app.token import admin_required
from app.dob import (add_user, user_task, task_delete, update)
from app.schema import (TaskSchema, InfoSchema,
                        UserSchema, UpdateSchema)
from app.util import data_now_json_str
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/create-user', endpoint='create_user', methods=['POST'])
@admin_required
def create_user():
    msg = ""
    user_schema = UserSchema()
    try:
        user = data_now_json_str(user_schema)
    except Exception as err:
        return jsonify({"missing": str(err)})

    if user['role'].upper() != "ADMIN":
        msg = add_user(user)
        return jsonify({"msg": msg})

    msg = "admin can add only EMPLOYEE AND MANAGER"
    return jsonify({"msg": msg})


@admin_bp.route('/create-task', endpoint='create_task', methods=['POST'])
@admin_required
def create_task():
    msg = ""
    task_schema = TaskSchema()
    try:
        user = data_now_json_str(task_schema)
        msg = user_task(user, "ADMIN")
    except Exception as err:
        return jsonify({"missing": str(err)})
    return jsonify({"msg": msg})


@admin_bp.route('/delete-task', endpoint='delete-task', methods=['DELETE'])
@admin_required
def delete_task():
    msg = ""
    info_schema = InfoSchema()
    try:
        task = data_now_json_str(info_schema)
        msg = task_delete(task)
    except Exception as err:
        return jsonify({"err": str(err)})

    return jsonify({"msg": msg})


@admin_bp.route('/update-task', endpoint='update-task', methods=['PATCH'])
@admin_required
def update_task():
    msg = ""
    update_schema = UpdateSchema()
    try:
        task = data_now_json_str(update_schema)
        msg = update(task)
    except Exception as err:
        return jsonify({"err": str(err)})
    return jsonify({"msg": msg})
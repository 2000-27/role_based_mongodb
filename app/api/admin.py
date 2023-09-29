from flask import jsonify, Blueprint
from app.token import admin_required
from app.dob import (add_user, user_task, task_delete, update_description, 
                     update_status) 

from app.schema import (TaskSchema, InfoSchema,
                        UserSchema, UpdateSchema, UpdateStatus, UpdateUser) 
from app.util import data_now_json_str
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/create-user', endpoint='create_user', methods=['POST'])
@admin_required
def create_user():
    msg = ""
    userschema = UserSchema()
    user = data_now_json_str(userschema)
    msg = add_user(user)
    return jsonify({"msg": msg})


@admin_bp.route('/create-task', endpoint='create_task', methods=['POST'])
@admin_required
def create_task():
    msg = ""
    task_schema = TaskSchema()
    user = data_now_json_str(task_schema)
    msg = user_task(user, "ADMIN")
    return jsonify({"msg": msg})


@admin_bp.route('/delete-task', endpoint='delete-task', methods=['DELETE'])
@admin_required
def delete_task():
    msg = ""
    info_schema = InfoSchema()
    task = data_now_json_str(info_schema)
    msg = task_delete(task)
    return jsonify({"msg": msg})


@admin_bp.route('/update_description', endpoint='update_desp', methods=['POST'])
@admin_required
def update_desp():
    msg = ""
    update_schema = UpdateSchema()
    user = data_now_json_str(update_schema)
    msg = update_description(user)
    return jsonify({"msg": msg})


@admin_bp.route('/update-status', endpoint='update_status', methods=['POST'])
@admin_required
def update_status():
    msg = ""
    status_Schema = UpdateStatus()
    user = data_now_json_str(status_Schema)
    msg = update_status(user)
    return jsonify({"msg": msg})


@admin_bp.route('/update-user', endpoint='update_status', methods=['POST'])
@admin_required
def update_user():
    msg = ""
    status_Schema = UpdateUser()
    user = data_now_json_str(status_Schema)
    msg = update_status(user)
    return jsonify({"msg": msg})

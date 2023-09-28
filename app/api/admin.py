from flask import request, jsonify, Blueprint
from app.token import admin_required
from app.dob import add_user, user_task, task_delete
from json import dumps, loads
from marshmallow import ValidationError
from app.schema import UserSchema, TaskSchema, LoginSchema, UpdateSchema
admin_bp = Blueprint("create-user", __name__)
assign_task = Blueprint("create-task", __name__)
delete_task = Blueprint("delete-task", __name__)
update_task = Blueprint("update-task", __name__)


@admin_bp.route('/create-user', methods=['POST'])
@admin_required
def create_user():
    msg = ""
    request_data = request.get_json()
    userschema = UserSchema()
    try:
        result = userschema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    data_now_json_str = dumps(result)
    user = loads(data_now_json_str)
    msg = add_user(user)
    return jsonify({"msg": msg})


@assign_task.route('/task', methods=['POST'])
@admin_required
def create_task():
    msg = ""
    request_data = request.get_json()
    task_schema = TaskSchema()
    try:
        result = task_schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    data_now_json_str = dumps(result)
    task = loads(data_now_json_str)
    msg = user_task(task)
    return jsonify({"msg": msg})


@delete_task.route('/task', methods=['DELETE'])
@admin_required
def deletetask():
    msg = ""
    request_data = request.get_json()
    delete_schema = LoginSchema()
    try:
        result = delete_schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    data_now_json_str = dumps(result)
    task = loads(data_now_json_str)
    msg = task_delete(task)
    return jsonify({"msg": msg})


@update_task.route('/task', methods=['PATCH'])
@admin_required
def updatetask():
    msg = ""
    request_data = request.get_json()
    delete_schema = UpdateSchema()
    try:
        result = delete_schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    data_now_json_str = dumps(result)
    task = loads(data_now_json_str)
    msg = update_task(task)
    return jsonify({"msg": msg})
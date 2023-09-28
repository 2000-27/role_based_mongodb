from flask import request, jsonify, Blueprint
from app.token import admin_required
from app.dob import add_user, user_task, task_delete, update_task
from json import dumps, loads
from marshmallow import ValidationError
from app.schema import UserSchema, TaskSchema, LoginSchema, UpdateSchema
admin_bp = Blueprint("create-user", __name__)
admin_task = Blueprint("create-task", __name__)


@admin_bp.route('/create-user', endpoint='create_user', methods=['POST'])
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


@admin_task.route('/create-task', endpoint='create_task', methods=['POST'])
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


@admin_task.route('/delete-task', endpoint='deletetask', methods=['DELETE'])
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


@admin_task.route('/update-task', endpoint='updatetask', methods=['PATCH'])
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
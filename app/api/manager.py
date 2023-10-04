from flask import jsonify, Blueprint
from app.token import manager_required
from app.dob import add_user, user_task, task_delete, update
from app.util import data_now_json_str
from app.schema import TaskSchema, UserSchema, InfoSchema
manager_bp = Blueprint("manager", __name__, url_prefix="manager")


@manager_bp.route('/create-user', endpoint='create_user', methods=['POST'])
@manager_required
def create_user():
    msg = ""
    userschema = UserSchema()
    user = data_now_json_str(userschema)
    msg = add_user(user)
    return jsonify({"message": msg})


@manager_bp.route('/create-task', endpoint='create_task', methods=['POST'])
@manager_required
def create_task():
    msg = ""
    task_schema = TaskSchema()
    task = data_now_json_str(task_schema)
    msg = user_task(task, "MANAGER")
    return jsonify({"message": msg})


@manager_bp.route('/delete-task', endpoint='delete-task', methods=['DELETE'])
@manager_required
def delete_task():
    msg = ""
    info_schema = InfoSchema()
    task = data_now_json_str(info_schema)
    print("task is ", task)
    msg = task_delete(task)
    return jsonify({"message": msg})


@manager_bp.route('/update-task', endpoint='update_task', methods=['POST'])
@manager_required
def update_task():
    msg = ""
    info_schema = InfoSchema()
    task = data_now_json_str(info_schema)
    msg = update(task)
    return jsonify({"message": msg})

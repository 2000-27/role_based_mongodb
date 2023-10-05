from flask import jsonify, Blueprint
from app.token import employee_required
from app.schema import ViewSchema, StatusSchema
from app.util import data_now_json_str
from app.dob import update
from bson.objectid import ObjectId
from app import mongo
employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


@employee_bp.route('/view-task', endpoint='view_task',  methods=['GET'])
@employee_required
def view_task():
    message = ""
    view_schema = ViewSchema()
    try:
        employee_detail = data_now_json_str(view_schema)     
    except Exception as err:
        return jsonify({"err": str(err)})
    user = mongo.db.users.find_one({'email': employee_detail['email']})
    if user is None:
        message = "their is no user, please singup"
        return jsonify({"message": message})

    try:
        task = mongo.db.tasks.find_one({'_id': ObjectId(employee_detail['task_id'])})
    except Exception:
        message = "Invalid object id "
        return jsonify({"message": message})

    if task is None:
        message = "no task is assign to him"
        print("hello")
        return jsonify({"message": message})
    return jsonify({"message": str(task)})


@employee_bp.route('/status-change', endpoint='change_status',
                   methods=['PATCH'])
@employee_required
def change_status():
    message = ""
    status_schema = StatusSchema()
    try:
        task = data_now_json_str(status_schema)
        message = update(task)
    except Exception as err:
        return jsonify({"err": str(err)})
    return jsonify({"message": message})

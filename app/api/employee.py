from flask import jsonify, Blueprint, request
from app.token import employee_required
from app.schema import StatusSchema
from app.token import token_decode
from app.util import data_now_json_str, serialize_doc, serialize_list
from app.dob import update
from bson.objectid import ObjectId
from app import mongo
employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


@employee_bp.route('/view-task', endpoint='view_task',  methods=['GET'])
@employee_required
def view_task():
    task_id = request.args.get('task_id', default=None)
    if task_id is not None:
        try:
            task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
            task = serialize_doc(task)

        except Exception:
            message = "Invalid ObjectId"
            return jsonify({"success": False, "message": message}), 400

        if task is None:
            message = "Invalid ObjectId"
            return jsonify({"success": False, "message": message}), 400

        return jsonify({"success": True, "details": task}), 200

    decoded_jwt = token_decode()
    user = mongo.db.users.find_one({'_id': ObjectId(decoded_jwt['user_id'])})
    all_task = list(mongo.db.tasks.find({'email': user['email']}))

    if len(all_task) == 0:
        return jsonify({"success": False, "message":
                        "No task is assign"}), 400

    alls_task = serialize_list(all_task)
    return jsonify({"success": True, "details": alls_task}), 200


@employee_bp.route('/status-change', endpoint='change_status',
                   methods=['PATCH'])
@employee_required
def change_status():
    message = ""
    status_schema = StatusSchema()
    try:
        task = data_now_json_str(status_schema)

        message = update(task, "employee")
        if message is True:
            return jsonify({"success": True, "message": "stutus is updated"}), 200
        return jsonify({"success": False, "message": message}), 400
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400

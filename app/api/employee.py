from flask import jsonify, Blueprint, request
from app.token import employee_required
from app.schema import StatusSchema
from app.util import data_now_json_str
from app.dob import update
from bson.objectid import ObjectId
from app import mongo

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


@employee_bp.route('/view-task', endpoint='view_task',  methods=['GET'])
@employee_required
def view_task():
    task_id = request.args.get('task_id', default="N/A")
    if task_id != "N/A":
        try:
            task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
        except Exception:
            message = "Invalid object id "
            return jsonify({"success": False, "message": message}), 403

        if task is None:
            message = "no task is assign to him"         
            return jsonify({"success": False, "message": message}), 403
        return jsonify({"success": True, "message": str(task)}), 200
    return jsonify({"success": False, "message": "task id is required"}), 403


@employee_bp.route('/status-change', endpoint='change_status',
                   methods=['PATCH'])
@employee_required
def change_status():
    message = ""
    status_schema = StatusSchema()
    try:
        task = data_now_json_str(status_schema)

        message = update(task)
        if message is True:
            return jsonify({"success": True, "message": "stutus is updated"}), 200
        return jsonify({"success": False, "message": message}), 403
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 403

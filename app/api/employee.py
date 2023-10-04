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
    msg = ""
    view_schema = ViewSchema()
    try:
        employee_detail = data_now_json_str(view_schema)     
    except Exception as err:
        return jsonify({"err": str(err)})    
    
    user = mongo.db.users.find_one({'email': employee_detail['email']})
    if user is None:
        msg = "their is no user, please singup"
        return jsonify({"msg": msg})

    try:
        task = mongo.db.tasks.find_one({'_id':ObjectId(employee_detail['task_id'])})
    except Exception:
        msg = "invalid object id "
        return jsonify({"msg": msg})

    if task is None:
        msg = "no task is assign to him"
        print("hello")
        return jsonify({"msg": msg})
    return jsonify({"msg": str(task)})


@employee_bp.route('/status-change', endpoint='change_status',
                   methods=['PATCH'])
@employee_required
def change_status():
    msg = ""
    status_schema = StatusSchema()
    task = data_now_json_str(status_schema)
    msg = update(task)
    return jsonify({"msg": msg})
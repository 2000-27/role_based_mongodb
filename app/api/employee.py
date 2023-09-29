from flask import jsonify, Blueprint
from app.token import employee_required
from app.schema import EmployeeSchema
from app.util import data_now_json_str
from app import mongo
employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


@employee_bp.route('/view-task', endpoint='view_task',  methods=['GET'])
@employee_required
def view_task():
    msg = ""
    employee_schema = EmployeeSchema()
    employee_detail = data_now_json_str(employee_schema)
    user = mongo.db.users.find_one({'email': employee_detail['email']})
    if user is None:
        msg = "their is no user, please singup"
        return jsonify({"msg": msg})
    task = mongo.db.tasks.find_one({'email': employee_detail['email']})
    if task is None:
        msg = "no task is assign to him"
        return jsonify({"msg": msg})    
   
    return jsonify({"msg": str(task)})
   

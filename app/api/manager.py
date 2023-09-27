from flask import request , jsonify , Blueprint 
from app.token import  manager_required
from app.dob import insert_data

admin_bp = Blueprint("create-user",__name__)
@admin_bp.route('/create-user', methods =['POST'])
@manager_required
def create():         
        json_body = request.get_json()
        user_name =json_body['user_name']
        email = json_body['email']
        password = json_body['password']
        confirm_password = json_body['confirm_password']
        role=json_body['role']
        msg=insert_data(user_name,password,confirm_password,email,role)
        return jsonify({"msg":msg})
      

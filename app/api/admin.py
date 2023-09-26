from flask import request , jsonify , Blueprint 

from app.token import  admin_required

admin_bp = Blueprint("create-user",__name__)
@admin_bp.route('/create-user', methods =['POST'])

@admin_required
def create():         
      json_body = request.get_json()
    #   username = json_body['username']
    #   email = json_body['email']
    #   userpassword = json_body['userpassword']
    #   confirmpwd = json_body['confirmpwd']
    #   role_id=json_body['role_id']
    #  msg=insert_into_db(username,email,userpassword,confirmpwd,role_id)
      msg="admin can access this record "
      return jsonify({"msg":msg})
      


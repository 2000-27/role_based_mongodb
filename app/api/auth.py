from flask import Blueprint, request , jsonify 
from app import db ,mongo 
from  app.dob import insert_data 
import jwt 

auth = Blueprint('auth', __name__, url_prefix='/auth')
@auth.route('/register', methods=['POST'])
def register():
     msg=""
     json_body = request.get_json() 
     user_name =json_body['user_name']
     email = json_body['email']
     password = json_body['password']
     confirm_password = json_body['confirm_password']
     role=json_body['role']
     msg=insert_data(user_name,password,confirm_password,email,role)       
     return jsonify({"msg":msg})


@auth.route('/login', methods=['POST'])
def login():
    try :  
      json_body = request.get_json() 
      user_name =json_body['user_name']
      email = json_body['email']
      password = json_body['password']
      is_user_exit=mongo.db.users.find_one({"email":email})
      user_id=is_user_exit['_id']
      if is_user_exit is None:
         return jsonify({'msg':"Signup Please"})                
      else:  
        encoded_jwt = jwt.encode({"user_id": str(user_id)}, "secret", algorithm="HS256")
        return jsonify(message="Login successfully" , access_token=encoded_jwt)
    except Exception as err:
        print("your errrorr is ",err)
         
        return jsonify("therer is error")
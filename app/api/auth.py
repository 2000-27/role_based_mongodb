from flask import Blueprint, request ,jsonify , current_app
from app import db ,mongo 
from datetime import datetime,timedelta
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
            confirm_password = json_body['confirmpwd']
            role_name=json_body['role_name']
            msg=insert_data(user_name,password,confirm_password,email,role_name)  
           
            if msg!="":
              return jsonify({"msg":msg})      
            else:   
                id = mongo.db.users.insert_one({   #users is my table name
                    "email": email,
                    "password":password,
                    "username": user_name,
                    "role_name":role_name,
                    }).inserted_id
                msg="successfully register"
                return jsonify({"msg":msg})



@auth.route('/login', methods=['POST'])
def login():
          try :  
            json_body = request.get_json() 
            user_name =json_body['user_name']
            email = json_body['email']
            password = json_body['password']
            is_user_exit=mongo.db.users.find_one({"email":email})
            if is_user_exit is None:
               return jsonify({'msg':"Signup Please"})                
            else:  
              encoded_jwt = jwt.encode({"email": email}, "secret", algorithm="HS256")
              return jsonify(message="Login successfully" , access_token=encoded_jwt)
          except Exception as err:
              print("your errrorr is ",err)
               
              return jsonify("therer is error")
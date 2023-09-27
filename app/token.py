import jwt
from flask import request , jsonify  
from . import mongo
from bson.objectid import ObjectId

def  token_decode(payload):
      payload = payload.split(" ")[1]
      decoded_jwt=jwt.decode(payload, "secret", algorithms=["HS256"])
      return decoded_jwt


def role():
   payload=request.headers["Authorization"]
   decoded_jwt=token_decode(payload)  
   user_id=decoded_jwt['user_id']
   bson_object=ObjectId(user_id)
   record=mongo.db.users.find_one({"_id":bson_object})
   return record


def token_required(f):
  def decorator():
        payload=request.headers["Authorization"]
        try:
           decoded_jwt=token_decode(payload)  
           user_email=decoded_jwt['email']
           print("user email is is is is is is is ",user_email)
           
        except  Exception as err:
              print("your error is ",err)
              return jsonify({"message": "Invalid token!"})
        return f()
  return decorator     




def admin_required(f):
     def decorator():
               record=role()
               if record['role'] != "ADMIN" :
                   raise Exception("anauthorised") 
               
               return f()
     return decorator   
           
           
               

def manager_required(f):
     def decorator():
               record=role()
               if record['role'] != "MANAGER" :
                   raise Exception("anauthorised") 
               
               return f()
     return decorator   
           
           
               
      

      


import jwt
from flask import request , jsonify 

def  token_decode(payload):
      payload = payload.split(" ")[1]
      decoded_jwt=jwt.decode(payload, "secret", algorithms=["HS256"])
     
      return decoded_jwt

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
            payload=request.headers["Authorization"]
            try:
               decoded_jwt=token_decode(payload)  
               print("your decoded jwt token",decoded_jwt)
               
                
               
               
            except  Exception as err:
                  print("your error is ",err)
                  return jsonify({"message": "Invalid token!"})
            return f()
     return decorator     
      


from .util import email_check , user_check , is_email_exit 
from . import mongo
def insert_data(user_name , password , confirm_password , email , role):
   is_email_valid=email_check(email)
   is_user_name_valid=user_check(user_name)
   is_user_exit=is_email_exit(email)  
   if is_user_exit :
        msg="this email is already register"
        return msg
   else:    
        if confirm_password != password: 
                msg="Password and confirm password should be same"
                return msg 
                    
        else:
            if is_email_valid:
                if  is_user_name_valid == False :
                        msg="Please enter a valid username"
                        return msg 
                else:
                    mongo.db.users.insert_one({  
                        "email": email,
                        "password":password,
                        "username": user_name,
                            "role":role,
                            }).inserted_id
                    msg="successfully register"
                    return msg
                
                
            else :
                    msg="Please enter a valid email address"
                    return msg
                    
                    
 
                  
            
            
        
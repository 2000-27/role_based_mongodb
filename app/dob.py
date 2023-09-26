from .util import email_check, user_check ,is_email_exit ,role_check
import bcrypt
def insert_data(user_name,password,confirm_password,email,role_name):
    is_email_valid=email_check(email)
    is_user_name_valid=user_check(user_name)
    is_role_exit=role_check(role_name) 
    is_user_exit=is_email_exit(email)
    if is_user_exit :
        msg="this email is already register "
        return msg
    else:    
        if confirm_password != password: 
                msg="Password and confirm password should be same"
                return msg  
                    
        else:
            if is_email_valid ==True:
                if  is_user_name_valid==False :
                        msg="Please enter a valid username"
                        return msg  
                else:
                      msg=""
                      return msg
                
            else :
                    msg="Please enter a valid email address"
                    return msg  
                
            
        
        
     
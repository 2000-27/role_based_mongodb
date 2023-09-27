from . import mongo
import re
def email_check(email):
    if not re.match(r'[^@]+@[^@]+\.[^@]+',email):  
           return False
    else :
          return True
        
    
def user_check(username):
        if not (re.match(r'[a-zA-Z0-9\s]+$',username)): 
            return False
        else :
          return True    


def is_email_exit(email):
     print("your email is",email)
     is_email_exit=mongo.db.users.find_one({"email":email})
     print("your email is exit in record is ",is_email_exit) 
     if is_email_exit != None :
         return True
     else :
         return False  

  

def role_check(user_role):
     role_is=mongo.db.role.find_one({"role_name":user_role})
     print("jdlkfjsdlkfjsl",role_is['role_name'])
     print("your role is ss  ",role_is)  
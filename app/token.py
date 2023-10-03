import jwt
from flask import request, abort, jsonify
from . import mongo
from bson.objectid import ObjectId


def token_decode(payload):
    payload = payload.split(" ")[1]
    decoded_jwt = jwt.decode(payload, "secret", algorithms=["HS256"])
    return decoded_jwt


def user_details(decoded_jwt):
    user_id = decoded_jwt['user_id']
    bson_object = ObjectId(user_id)
    user = mongo.db.users.find_one({"_id": bson_object})
    return user


def valid_token():
    payload = request.headers["Authorization"]
    try:
        decoded_jwt = token_decode(payload)
    except Exception:
        return jsonify({"message": "Invalid token!"})
    user = user_details(decoded_jwt)
    return user
   

def admin_required(f):
    def decorator():
        user = valid_token()
        if user['role'] != "ADMIN":
            abort(401)
        return f()
    return decorator


def manager_required(f):
    def decorator():
        user = valid_token()
        if user['role'] != "MANAGER":
            abort(401)
        return f()
    return decorator


def employee_required(f):
    def decorator():
        user = valid_token()
        if user['role'] != "EMPLOYEE":
            abort(401)
        return f()
    return decorator

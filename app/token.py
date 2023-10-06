import jwt
from flask import request, abort, jsonify
from . import mongo
from bson.objectid import ObjectId


def token_decode():
    try:
        payload = request.headers["Authorization"]
        payload = payload.split(" ")[1]
        decoded_jwt = jwt.decode(payload, "secret", algorithms=["HS256"])
        user = mongo.db.users.find_one({"_id": ObjectId(decoded_jwt['user_id'])
                                        })
        if user is None:
            raise Exception("invalid token")
    except Exception:
        raise Exception("Please enter a valid token")
    return decoded_jwt


def user_details(decoded_jwt):
    user_id = decoded_jwt['user_id']
    bson_object = ObjectId(user_id)
    user = mongo.db.users.find_one({"_id": bson_object})
    return user


def admin_required(f):
    def decorator():
        try:
            decoded_jwt = token_decode()
            
            user = user_details(decoded_jwt)
            if user['role'].lower() != 'admin':
                return jsonify({"message": "401 Unauthorized", "success": False}), 401
        except Exception as err:
            return jsonify({"message": str(err), "success": False}), 400
        return f()
    return decorator


def manager_required(f):
    def decorator():
        try:
            decoded_jwt = token_decode()
            user = user_details(decoded_jwt)
            if user['role'].lower() != 'manager':
                return jsonify({"message": "401 Unauthorized", "success": False}), 401
        except Exception as err:
            return jsonify({"message": str(err), "success": False}), 400
        return f()
    return decorator


def employee_required(f):
    def decorator():
        try:
            decoded_jwt = token_decode()
            user = user_details(decoded_jwt)
            if user['role'] != 'employee':
                return jsonify({"message": "401 Unauthorized", "success": False}), 401
        except Exception as err:
            return jsonify({"message": str(err), "success": False}), 400
        return f()
    return decorator

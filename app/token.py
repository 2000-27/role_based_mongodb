import jwt
from flask import request, abort, jsonify
from . import mongo
from bson.objectid import ObjectId


def token_decode():
    payload = request.headers["Authorization"]
    try:
        payload = payload.split(" ")[1]
        decoded_jwt = jwt.decode(payload, "secret", algorithms=["HS256"])
        user = mongo.db.users.find_one({"_id": ObjectId(decoded_jwt['user_id'])
                                        })
        if user is None:
            raise Exception("invalid token")
    except Exception:
        raise Exception("invalid token")
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
            print(decoded_jwt)
            user = user_details(decoded_jwt)
            if user['role'].lower() != 'admin':
                abort(401)
        except Exception as err:
            return jsonify({"message": str(err), "success": False}), 403
        return f()
    return decorator


def manager_required(f):
    def decorator():
        try:
            decoded_jwt = token_decode()
            user = user_details(decoded_jwt)
            if user['role'].lower() != 'manager':
                abort(401)
        except Exception as err:
            return jsonify({"message": str(err), "success": False}), 403
        return f()
    return decorator


def employee_required(f):
    def decorator():
        try:
            decoded_jwt = token_decode()
            user = user_details(decoded_jwt)
            if user['role'] != 'employee':
                abort(401)
        except Exception as err:
            return jsonify({"message": str(err), "success": False}), 403
        return f()
    return decorator

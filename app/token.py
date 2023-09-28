import jwt
from flask import request, abort
from . import mongo
from bson.objectid import ObjectId


def token_decode():
    payload = request.headers["Authorization"]
    payload = payload.split(" ")[1]
    decoded_jwt = jwt.decode(payload, "secret", algorithms=["HS256"])
    return decoded_jwt


def user_role():
    decoded_jwt = token_decode()
    user_id = decoded_jwt['user_id']
    bson_object = ObjectId(user_id)
    user = mongo.db.users.find_one({"_id": bson_object})
    return user


def admin_required(f):
    def decorator():
        record = user_role()
        if record['role'] != "ADMIN":
            abort(401)
        return f()
    return decorator


def manager_required(f):
    def decorator():
        record = user_role()
        if record['role'] != "MANAGER":
            abort(401)
        return f()
    return decorator

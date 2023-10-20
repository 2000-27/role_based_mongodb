from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from json import dumps, loads
from app.util import encoded_jwt
from app.schema import UserSchema, LoginSchema
from app.dob import add_client

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["POST"])
def register():
    message = ""
    request_data = request.get_json()
    user_schema = UserSchema()
    try:
        result = user_schema.load(request_data)
        data_now_json_str = dumps(result)
        user = loads(data_now_json_str)
        message, response = add_client(user)
    except ValidationError as err:
        return jsonify({"success": False, "message": str(err)}), 400

    if response:
        return jsonify({"success": True, "message": message}), 200
    return jsonify({"success": False, "message": message}), 400


@auth.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()
    login_schema = LoginSchema()
    try:
        result = login_schema.load(request_data)
        data_now_json_str = dumps(result)
        data = loads(data_now_json_str)
        message, response = encoded_jwt(data)
    except ValidationError as err:
        return jsonify({"success": False, "message": str(err)}), 400
    if response:
        return jsonify({"success": True, "message": message}), 200
    return jsonify({"success": False, "message": message}), 400

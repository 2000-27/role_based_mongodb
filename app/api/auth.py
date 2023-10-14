from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from json import dumps, loads
from app import mongo
import datetime
from app.config import algorithum
from flask_bcrypt import check_password_hash
from app.schema import UserSchema, LoginSchema
from app.dob import add_user
import jwt
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['POST'])
def register():
    message = ""
    request_data = request.get_json()
    user_schema = UserSchema()
    try:
        result = user_schema.load(request_data)
    except ValidationError as err:
        return jsonify({"success": False, "message": str(err)}), 400
    data_now_json_str = dumps(result)
    user = loads(data_now_json_str)
    if user['role'] == 'manager':
        message = add_user(user)
        if message is True:
            return jsonify({"success": True,
                            "message": "Register sucessfully"}), 200
        return jsonify({"success": False, "message": message}), 400
    message = "Manager can only register"
    return jsonify({"success": False, "message": message}), 400


@auth.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    login_schema = LoginSchema()
    try:
        result = login_schema.load(request_data)
    except ValidationError as err:
        return jsonify({"success": False, "message": str(err)}), 400

    data_now_json_str = dumps(result)
    data = loads(data_now_json_str)
   
    user = mongo.db.users.find_one({"email": data['email']})
    
    if user is None:
        return jsonify({"success": False,
                        'message': "There is no user, Please signup"}), 400

    if check_password_hash(user['password'], data['password']):
        user_id = user['_id']
        payload = {"user_id": str(user_id), "user_role": str(user['role']),
                   "organization_name": str(user['organization_name']),
                   "exp": datetime.datetime.utcnow() +
                   datetime.timedelta(hours=10)}
        encoded_jwt = jwt.encode(payload, "secret", algorithm=algorithum)
        details = {"access token": str(encoded_jwt),
                   "user_id": str(user['_id']) }
        return jsonify({"success": True, "message": "Login successfully",
                       "details": details}), 200
    return jsonify({"success": False, 'message':
                    "Enter the correct password"}), 400

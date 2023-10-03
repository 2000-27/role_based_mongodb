from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from json import dumps, loads
from app import mongo
from app.config import algor
from app.schema import UserSchema, LoginSchema
from app.dob import add_user
import jwt

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['POST'])
def register():
    msg = ""
    request_data = request.get_json()
    user_schema = UserSchema()
    try:
        result = user_schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    data_now_json_str = dumps(result)
    user = loads(data_now_json_str)
    msg = add_user(user)
    return jsonify({"msg": msg})


@auth.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    login_schema = LoginSchema()
    try:
        result = login_schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    data_now_json_str = dumps(result)
    data = loads(data_now_json_str)
    user = mongo.db.users.find_one({"email": data['email']})
    if user is None:
        return jsonify({'msg': "there is no user ,please signup"})
    user_id = user['_id']
    encoded_jwt = jwt.encode({"user_id": str(user_id)},
                             "secret", algorithm=algor)
    return jsonify(message="Login successfully", access_token=encoded_jwt)

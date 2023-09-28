from flask import request, jsonify, Blueprint
from app.token import manager_required
from app.dob import add_user
from json import dumps, loads
from marshmallow import ValidationError
from app.schema import UserSchema
admin_bp = Blueprint("create-user", __name__)


@admin_bp.route('/create-user', methods=['POST'])
@manager_required
def create():
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

from flask import jsonify, Blueprint
from app import mongo
from app.dob import organization_info
from app.token import client_required
from app.schema import SendTaskSchema
from app.util import data_now_json_str, mail_send

organization_bp = Blueprint("organization", __name__, url_prefix="/organization")

client_bp = Blueprint("client", __name__, url_prefix="/client")


@client_bp.route("/view-list", endpoint="view_list", methods=["GET"])
@client_required
def view_list():
    all_organization_list = [
        x["organization_name"] for x in list(mongo.db.orgnizations.find())
    ]
    data = organization_info(all_organization_list)
    return jsonify({"success": True, "organization-list": data}), 200


@client_bp.route("/send-purposal", endpoint="purposal", methods=["POST"])
@client_required
def purposal():
    task_schema = SendTaskSchema()
    try:
        task = data_now_json_str(task_schema)
        company = mongo.db.orgnizations.find_one(
            {"organization_name": task["organization_name"]}
        )
        print(task, company)
        if company is None:
            return (
                jsonify({"success": False, "message": "Enter a valid company name"}),
                400,
            )
        mail_send(task, "client", "purposal")
    except Exception as err:
        return jsonify({"success": False, "message": str(err)}), 400
    return jsonify({"success": True, "message": "You get a mail on your email Id"}), 200

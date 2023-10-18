from flask import jsonify, Blueprint
from app import mongo
from app.dob import organization_info

organization_bp = Blueprint("organization", __name__, url_prefix="/organization")


@organization_bp.route("/view-list", endpoint="view_list", methods=["GET"])
def view_list():
    all_organization_list = [
        x["organization_name"] for x in list(mongo.db.orgnizations.find())
    ]
    data = organization_info(all_organization_list)
    return jsonify({"success": True, "organization-list": data}), 200

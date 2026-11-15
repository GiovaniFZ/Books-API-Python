from flask import Blueprint, jsonify

user_routes_bp = Blueprint("user_routes", __name__)

@user_routes_bp.route("/api/v1/register", methods=["POST"])
def registry_user():
    return jsonify({"route": "Register" })

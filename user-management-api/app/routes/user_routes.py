from flask import Blueprint, jsonify, request

from app.services.user_service import create_user, get_all_users


user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("", methods=["POST"])
def create_user_route():
    data = request.get_json()

    user = create_user(
        name=data.get("name"),
        email=data.get("email"),
        role=data.get("role")
    )

    return jsonify({
        "success": True,
        "data": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 201


@user_bp.route("", methods=["GET"])
def get_users():
    users = get_all_users()

    return jsonify({
        "success": True,
        "data": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
            for user in users
        ]
    }), 200
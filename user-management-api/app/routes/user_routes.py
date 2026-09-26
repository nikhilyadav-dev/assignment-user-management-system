from flask import Blueprint, jsonify, request
from app.utils.validators import is_valid_email


from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id
)

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
    search = request.args.get("search")

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    users, total = get_all_users(
        search=search,
        page=page,
        limit=limit
    )

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
        ],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total
        }
    }), 200


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    return jsonify({
        "success": True,
        "data": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200
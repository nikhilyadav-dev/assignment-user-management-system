from flask import Blueprint, jsonify, request
from app.utils.validators import is_valid_email


from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    email_exists
)

user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("", methods=["POST"])
def create_user_route():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")
    role = data.get("role")

    if not name or not email or not role:
        return jsonify({
            "success": False,
            "error": "Name, email, and role are required"
        }), 400

    if not is_valid_email(email):
        return jsonify({
            "success": False,
            "error": "Invalid email format"
        }), 400

    if email_exists(email):
      return jsonify({
        "success": False,
        "error": "Email already exists"
    }), 409

    user = create_user(
        name=name,
        email=email,
        role=role
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

    if page < 1:
     return jsonify({
        "success": False,
        "error": "Page must be greater than 0"
    }), 400

    if limit < 1 or limit > 100:
      return jsonify({
        "success": False,
        "error": "Limit must be between 1 and 100"
    }), 400

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
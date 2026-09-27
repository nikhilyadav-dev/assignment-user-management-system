from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.auth import admin_required

from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
  
)

from app.errors.exceptions import (
    NotFoundError,
    ValidationError,
)
 
user_bp = Blueprint("users", __name__, url_prefix="/users")


# CREAT USER ROUTE
@user_bp.route("", methods=["POST"])
@admin_required
def create_user_route():

    data = request.get_json(silent=True)

    # Body Required Validation
    if not data:
      raise ValidationError(
               "Request body is required")
    

    user = create_user(
        name = data.get("name"),
        email = data.get("email"),
        role = data.get("role"),
        password = data.get("password")
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


# GET USERS ROUTE
@user_bp.route("", methods=["GET"])
@jwt_required()
def get_users():
    search = request.args.get("search")

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    if page < 1:
      raise ValidationError( "Page must be greater than 0")
 

    if limit < 1 or limit > 100:
      raise ValidationError( "Limit must be between 1 and 100")

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

# GET USER BY ID ROUTE
@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    user = get_user_by_id(user_id)

    # Validation 
    if user is None:
          raise NotFoundError("User not found")

    return jsonify({
        "success": True,
        "data": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200
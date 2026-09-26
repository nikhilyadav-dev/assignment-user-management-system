from flask import Blueprint, jsonify, request
from app.utils.validators import is_valid_email
from app.services.auth_service import hash_password

from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    email_exists
)

from app.errors.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError
)
 
user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("", methods=["POST"])
def create_user_route():
    data = request.get_json(silent=True)

    if not data:
      raise ValidationError(
               "Request body is required")
       

    name = data.get("name")
    email = data.get("email")
    role = data.get("role")
    password = data.get("password")

    if not name or not email or not role or not password:
        raise ValidationError(
        "Name, email, and role, password are required"
    )

    if not is_valid_email(email):
        raise ValidationError(
        "Invalid email format"
    )
    if email_exists(email):
      raise ConflictError("Email already exists")

    password_hash = hash_password(password)

    user = create_user(
        name=name,
        email=email,
        role=role,
        password_hash=password_hash
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


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)

  

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
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from app.errors.exceptions import UnauthorizedError, ValidationError
from app.services.auth_service import authenticate_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

### LOGIN USER ROUTE
@auth_bp.route("/login", methods=["POST"])

def login():
    data = request.get_json(silent=True)

    # Request Body Validation
    if not data:
        raise ValidationError("Request body is required")

    email = data.get("email")
    password = data.get("password")

    # Required Fields Validation
    if not email or not password:
        raise ValidationError("Email and password are required")

    user = authenticate_user(email, password)

    if user is None:
        raise UnauthorizedError()

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "success": True,
        "data": {
            "access_token": access_token
        }
    }), 200
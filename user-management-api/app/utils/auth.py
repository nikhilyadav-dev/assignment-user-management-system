from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request

from app.errors.exceptions import ForbiddenError


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        claims = get_jwt()

        if claims.get("role") != "admin":
            raise ForbiddenError("Admin access required")

        return fn(*args, **kwargs)

    return wrapper
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.user import User


def hash_password(password):
    return generate_password_hash(password)


def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)


def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()

    if user is None:
        return None

    if not user.password_hash:
        return None

    if not verify_password(user.password_hash, password):
        return None

    return user
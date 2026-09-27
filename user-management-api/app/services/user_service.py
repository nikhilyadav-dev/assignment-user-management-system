from sqlalchemy import or_

from app.extensions import db
from app.models.user import User

from app.services.auth_service import hash_password 
from app.utils.validators import is_valid_email 
from app.errors.exceptions import ConflictError, ValidationError

# CREATE USER SERVICE
def create_user(name, email, role, password):

    # Reuired Field
    if not name or not email or not role or not password:
        raise ValidationError(
        "Name, email, role, and password are required"
    )

    # Email Format Validation
    if not is_valid_email(email):
        raise ValidationError(
        "Invalid email format"
    )

    # Duplicate Email Validation
    if email_exists(email):
      raise ConflictError("Email already exists")

    # Password Hashing
    password_hash = hash_password(password)

    user = User(
        name=name,
        email=email,
        role=role,
        password_hash=password_hash
    )

    # DB Faliure Handling
    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return user

# GET ALL USERS SERVICE
def get_all_users(search=None, page=1, limit=10):
    query = User.query

    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            or_(
                User.name.ilike(search_pattern),
                User.email.ilike(search_pattern)
            )
        )

    total = query.count()

    offset = (page - 1) * limit

    users = (
        query
        .order_by(User.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return users, total

# GET USER BY ID SERVICE
def get_user_by_id(user_id):
    return db.session.get(User, user_id)

# UNIQUE EMAIL HELPING FUNCTION
def email_exists(email):
    return User.query.filter_by(email=email).first() is not None
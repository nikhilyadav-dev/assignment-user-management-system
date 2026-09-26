from sqlalchemy import or_

from app.extensions import db
from app.models.user import User


def create_user(name, email, role):
    user = User(
        name=name,
        email=email,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return user


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


def get_user_by_id(user_id):
    return db.session.get(User, user_id)

def email_exists(email):
    return User.query.filter_by(email=email).first() is not None
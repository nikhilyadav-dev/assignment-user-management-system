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


def get_all_users():
    return User.query.all()
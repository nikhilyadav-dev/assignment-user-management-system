import click
from flask.cli import with_appcontext

from app.extensions import db
from app.models.user import User
from app.services.auth_service import hash_password


@click.command("seed")
@with_appcontext
def seed():
    existing_admin = User.query.filter_by(
        email="admin@example.com"
    ).first()

    if existing_admin:
        click.echo("Admin user already exists.")
        return

    admin = User(
        name="Admin",
        email="admin@example.com",
        role="admin",
        password_hash=hash_password("Admin@123")
    )

    db.session.add(admin)
    db.session.commit()

    click.echo("Admin user created successfully")
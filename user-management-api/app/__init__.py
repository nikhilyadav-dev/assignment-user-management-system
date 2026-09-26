from flask import Flask

from app.config import Config
from app.extensions import db, migrate, jwt
from app.routes.user_routes import user_bp
from app.errors.handlers import register_error_handlers
from app.logging_config import configure_logging
from app.routes.auth_routes import auth_bp
from app.commands import seed



def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)

    jwt.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    register_error_handlers(app)

    app.cli.add_command(seed)

    return app
from flask import Flask

from app.config import Config
from app.extensions import db, migrate
from app.routes.user_routes import user_bp
from app.errors.handlers import register_error_handlers



def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)

    app.register_blueprint(user_bp)

    register_error_handlers(app)

    return app
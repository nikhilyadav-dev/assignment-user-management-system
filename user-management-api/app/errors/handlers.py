from flask import jsonify

from app.errors.exceptions import AppError
from app.extensions import jwt


def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({
            "success": False,
            "error": error.message
        }), error.status_code


    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({
            "success": False,
            "error": "Resource not found"
        }), 404

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception(error)

        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

    @jwt.unauthorized_loader
    def handle_missing_token(error): 
        return jsonify({ "success": False, "error": error }), 401


    @jwt.invalid_token_loader
    def handle_invalid_token(error):
        return jsonify({ "success": False, "error": error }), 401

    @jwt.expired_token_loader
    def handle_expired_token(jwt_header, jwt_payload):
        return jsonify({ "success": False, "error": "Token has expired" }), 401
from flask import jsonify

from app.errors.exceptions import AppError


def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({
            "success": False,
            "error": error.message
        }), error.status_code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception(error)

        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500
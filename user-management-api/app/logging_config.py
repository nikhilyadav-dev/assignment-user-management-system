import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging(app):
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    app.logger.setLevel(log_level)

    app.logger.handlers.clear()

    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)
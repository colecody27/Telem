import logging
from logging.handlers import RotatingFileHandler
import os

# Log file location
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "service.log")

# Create a logger
logger = logging.getLogger("service")
logger.setLevel(logging.INFO)  # Default log level

# Avoid adding handlers multiple times
if not logger.handlers:
    # Console handler (prints logs to stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler with rotation (1MB per file, keep 3 backups)
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)
    file_handler.setLevel(logging.INFO)
    
    # Log message format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def init_app(app):
    """
    Integrate the logger with a Flask app's built-in logger.
    
    Usage:
        app = Flask(__name__)
        init_app(app)
    """
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)

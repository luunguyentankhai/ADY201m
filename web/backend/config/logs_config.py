import logging
from logging import handlers
import logging.config
from web.backend.config.dir_config import LOG_DIR
from logging.handlers import RotatingFileHandler

LOG_FILE = LOG_DIR / "web.log"

LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers" : False,
        "formatters": {
            "web_formatter": {
                "format": "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "web_formatter",
                "level": "INFO",
                },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(LOG_FILE),
                "maxBytes": 5 * 1024 * 1024,
                "backupCount": 3,
                "encoding": "utf-8",
                "formatter": "web_formatter",
                "level": "INFO",
                },
            },
        "loggers": {
            "api_logger": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
                },
            "uvicorn.error": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
                }
            }
        }

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("api_logger")

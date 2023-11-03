import logging
from logging.config import dictConfig
from app.core.settings.base import AppSettings


def obfuscated(email: str, obfuscated_length: int) -> str:
    chars = email[:obfuscated_length]
    first, last = email.split("@")
    return chars + ("*" * (len(first) - obfuscated_length)) + "@" + last


class EmailObfuscationFilter(logging.Filter):

    def __init__(self, name: str = "", obfuscated_length: int = 2) -> None:
        super().__init__(name)
        self.obfuscated_length = obfuscated_length

    def filter(self, record: logging.LogRecord) -> bool:
        if "email" in record.__dict__:
            record.email = obfuscated(record.email, self.obfuscated_length)
        return True


def configure_logging(settings: AppSettings) -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if settings.env_state == "dev" else 32,
                    "default_value": "-"
                },
                "email_obfuscation": {
                    "()": EmailObfuscationFilter,
                    "obfuscated_length": 2 if settings.env_state == "dev" else 0
                }
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s %(msecs)03d %(levelname)-8s %(correlation_id)s %(name)s %(lineno)d %("
                              "message)s"
                }
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id"]
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": "tasktracker.log",
                    "maxBytes": 1024 * 1024,
                    "backupCount": 2,
                    "encoding": "utf8",
                    "filters": ["correlation_id"]
                }
            },
            "loggers": {
                "uvicorn": {
                    "handlers": ["default", "rotating_file"],
                    "level": "INFO"
                },
                "app": {
                    "handlers": ["default", "rotating_file"],
                    "level": "DEBUG" if settings.env_state == "dev" else "INFO",
                    "propagate": False,
                },
                "sqlalchemy": {
                    "handlers": ["default"],
                    "level": "WARNING"
                },
            },
        }
    )

import logging
import logging.config


def configure_logging(level: str) -> None:
    configuration = {
        "version": 1,
        "disable_existing_loggers": True,  # this is default
        "formatters": {
            "json": {
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
        },
        "root": {
            "level": level,
            "handlers": ["console"],
        }
    }

    logging.config.dictConfig(configuration)

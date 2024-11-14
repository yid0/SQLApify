from logger.logger_factory import LoggerFactory
import logging
def load_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,           
        "formatters": {
            "dynamic": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "dynamic",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {  
                "level": "INFO",
                "handlers": [],
                "propagate": False,
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": [],
                "propagate": False,
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": [],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": [],
                "propagate": False,
            },
            "fastapi": {  
                "level": "INFO",
                "handlers": [],
                "propagate": False,
            },
        },
    }

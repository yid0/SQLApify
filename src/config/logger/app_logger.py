import logging
from config.configuration import Configuration
from pyglog import LoggerFactory
from .uvicorn_config import load_config


class AppLogger:
    # TODO: Fix logger
    def __init__(self, name):
        self.name = name
        self.logger = self._get_factory().create_logger()
        self._setup_logger()

    def _setup_logger(self):
        try:
            loggerConfig = Configuration.get_instance(key="logger")
            loggerConfig.load()
            self.config = load_config()

            self.config["formatters"] = {
                "dynamic": {
                    "()": type(self.logger_factory.get_formatter()),
                    "format": self.logger_factory.get_format(),
                },
            }
            # self.logger.propagate = False
            logging.config.dictConfig(self.config)

        except Exception as e:
            print(f"Cannot setup the application logger: {str(e)}")

    def _get_factory(self):
        self.logger_factory = LoggerFactory.get_logger_factory(self.name)
        return self.logger_factory

    def get_logger(self) -> logging.Logger:
        return self.logger

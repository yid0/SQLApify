from .base_logger_factory import BaseLoggerFactory
import logging

class StandardLoggerFactory(BaseLoggerFactory):
    name: str = "standard_logger"
        
    def __init__(self, name):
        self.name = name
        self._formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        super().__init__(self.name)
        
        
    def create_logger(self) -> logging.Logger:
        from os import getenv
        self._handler.setFormatter(self._formatter)
        self._logger.addHandler(self._handler)
        self._logger.setLevel(getenv("LOG_LEVEL", logging.INFO))
        return self._logger

    def get_formatter(self):
        return self._formatter
    
    def get_format(self):
        return self.get_formatter()

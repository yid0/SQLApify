import logging
from .base_logger_factory import BaseLoggerFactory

class OpenSearchLoggerFactory(BaseLoggerFactory):
    name: str ="opensearch_logger"
    
    def __init__(self, name):
        self.name = name
        self._formatter = logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
        super().__init__(name)        
        
    def create_logger(self) -> logging.Logger:
        from os import getenv
        self._handler.setFormatter(self._formatter)
        self._logger.addHandler(self._handler)
        self._logger.setLevel(getenv("LOG_LEVEL", logging.INFO))
        return self.logger

    def get_formatter(self) -> logging.Formatter:
        return self._formatter    
    
    def get_format(self):
        return self.get_formatter()
import logging
from ecs_logging import StdlibFormatter
from .base_logger_factory import BaseLoggerFactory

class ElasticsLoggerFactory(BaseLoggerFactory):   
    
    _name: str = "ecs_logger"
    
    def __init__(self, name):
        self._formatter = StdlibFormatter()
        super().__init__(name)
                
    def create_logger(self) -> logging.Logger:
        from os import getenv
        self._handler.setFormatter(self._formatter)
        self._logger.addHandler(self._handler)
        self._logger.setLevel(getenv("LOG_LEVEL", logging.INFO))
        return self._logger
    
    def get_formatter(self) -> any:
        return self._formatter
    
    def get_format(self):
        return getattr(self.get_formatter(), '_fmt', None)
from abc import ABC
import logging

class BaseLoggerFactory(ABC):
    
    _logger: logging.Logger
    _handler: logging.StreamHandler
    _formatter: logging.Formatter | None
    
    def __init__(self, name: str):     
        self._logger = logging.getLogger(name)
        self._handler = logging.StreamHandler()

    @classmethod
    def create_logger(self) -> logging.Logger:
        pass
    
    @classmethod
    def get_formatter(self) -> logging.Formatter :
        pass
    
    @classmethod
    def get_format(self) -> str :
        pass

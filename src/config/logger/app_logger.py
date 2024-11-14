import logging
from config.configuration import Configuration
from logger.logger_factory import LoggerFactory
from .logger_config import LoggerConfig
from .uvicorn_config import load_config

class AppLogger:
    _instances = {}
    
    def __new__(cls, name):
        if name not in cls._instances:
            cls._instances[name] = super(AppLogger, cls).__new__(cls)
            cls._instances[name].name = name
            cls._instances[name]._setup_logger()
        return cls._instances[name]
    
    def _setup_logger(self):
        try:

            loggerConfig = Configuration(LoggerConfig)
            
            loggerConfig.load()

            self.config = load_config()    
            
            self.config["formatters"] = {
                "dynamic": { 
                    "()": type(self._instances[self.name].logger_factory.get_formatter()),
                    "format": self._instances[self.name].logger_factory.get_format()
                },
            }
            
            logging.config.dictConfig(self.config)
            
        except Exception as e:
            print(f"Cannot setup the application logger: {str(e)}")
    
    def _get_factory(self):

        self._instances[self.name].logger_factory = LoggerFactory.get_logger_factory(self.name)
        return self._instances[self.name].logger_factory
       
    
    def get_logger(self) -> logging.Logger:       
        self.logger = self._instances[self.name]._get_factory().create_logger() 
        return self.logger


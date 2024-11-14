from enum import Enum
from config.env_value_mixin import EnvMixin

class LoggerConfig(EnvMixin, Enum):    
        
    APP_LOG_LEVEL= ("LOG_LEVEL", "log_level")
    APP_LOG_FORMAT= ("LOG_FORMAT", "log_format")
    
    def load(self):
        from os import getenv

        self.env_dict = { 
                        
            LoggerConfig.APP_LOG_FORMAT.alias: getenv(str(LoggerConfig.APP_LOG_FORMAT.env_name), "standard"),
            LoggerConfig.APP_LOG_LEVEL.alias: getenv(str(LoggerConfig.APP_LOG_LEVEL.env_name), "INFO")
        }    
        
        self.validate(self, self.env_dict)  

        return self.env_dict
    
    def validate(self, env_values):
        from .logger_config_validator import LoggerConfigValidator
        return bool(LoggerConfigValidator(**env_values))
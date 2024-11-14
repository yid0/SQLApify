from enum import Enum
from .base_configuration import BaseConfiguration 

class Configuration(BaseConfiguration):
    
    def __init__(self, config_type: Enum):
        self.config_type = config_type
    
    def load(self):
        return self.config_type.load(self.config_type)
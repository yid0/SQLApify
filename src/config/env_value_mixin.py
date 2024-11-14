from abc import  abstractmethod

class EnvMixin:
     
    DB_PROTOCOL = ("DB_PROTOCOL", "protocol")
    DB_HOST= ("DB_HOST" , "host")
    DB_PORT= ("DB_PORT", "port")
    DB_NAME= ("DB_NAME", "database")
    DB_SCHEMA= ("DB_SCHEMA", "schema")
    DB_USERNAME= ("DB_USERNAME", "username")
    DB_PASSWORD= ("DB_PASSWORD", "password")
    
    env_dict: dict
    
    @property
    def env_name(self):
        """Get env varibale name."""
        return self.value[0]

    @property
    def alias(self):
        """Get the alias name used on the application"""
        return self.value[1]
    
    @abstractmethod
    def load(self):
        """
        Load the needed configuration class        
        """
    @abstractmethod
    def validate(self, **env_values):
        pass

    @classmethod
    def check_value(cls, value: str):
        return value in cls._value2member_map_
    
    @classmethod
    def get_all_keys(self):
        return [item.name for item in self]
    
    
    @classmethod
    def get_all_values(self):
        return [item.value for item in self]

    def get_env(key: str):
        from os import getenv
        return getenv(str(key))
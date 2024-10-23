import os
from enum import Enum
from db import DbType
from db.provider import SQLiteDatabase

class UserCredentialConfig(str, Enum):
    APP_USER="APP_USER"
    APP_PASSWORD="APP_PASSWORD"
 
class PostgresConfig(str, Enum):
    POSTGRES_PROTOCOL="POSTGRES_PROTOCOL"
    POSTGRES_HOST="POSTGRES_HOST"
    POSTGRES_PORT="POSTGRES_PORT"
    POSTGRES_DATABASE="POSTGRES_DATABASE"
    POSTGRES_PASSWORD="POSTGRES_PASSWORD"
    
    @staticmethod
    def load():
        username = os.getenv(UserCredentialConfig.APP_USER)
        password = os.getenv(UserCredentialConfig.APP_PASSWORD)
        protocol = os.getenv(PostgresConfig.POSTGRES_PROTOCOL)
        host = os.getenv(PostgresConfig.POSTGRES_HOST)
        port = os.getenv(PostgresConfig.POSTGRES_PORT)
        db_name = os.getenv(PostgresConfig.POSTGRES_DATABASE)
                
        if username is None or password is None:
            raise Exception("Please set APP_USER and APP_PASSWORD as environment variables.")
        
        if not isinstance(username, str) or not isinstance(password, str):
            raise TypeError("username and password must be strings.")        
        return (protocol,host, port, db_name, username, password)
    
class Configuration:
        
        def load_config(self, db_type: DbType):
            match self.db_type:
                case DbType.POSTGRES:
                    return  PostgresConfig.load()
                case DbType.SQLITE:
                    return SQLiteDatabase(self.connection)
                case _:
                    raise ValueError("Unsupported database type")
         
        
        
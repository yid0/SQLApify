from repository import DbType, Connection, Credential
from repository.provider import PostgresConnection
from repository.provider import SQLiteConnection
from config.postgres import PostgresAdminConfig 

class ConnectionFactory:
    
    @staticmethod
    def create_connection(db_type: DbType, **kwargs) -> Connection:
        print(kwargs['kwargs'])
        match db_type:
            case DbType.POSTGRES: 
                return PostgresConnection(
                    protocol=PostgresAdminConfig.env_dict["protocol"],
                    host=PostgresAdminConfig.env_dict["host"],
                    port=PostgresAdminConfig.env_dict["port"],
                    db_name=kwargs['kwargs'].get("database"),
                    credential=Credential(username= kwargs['kwargs'].get("username"),
                                          password= kwargs['kwargs'].get("password")))
            case DbType.SQLITE :
                return SQLiteConnection(db_name=kwargs["db_name"])
            case _ :
                raise ValueError(f"Unsupported database type: {db_type}")
from db import DbType, Connection
from db.provider import PostgresConnection
from db.provider import SQLiteConnection

class ConnectionFactory:
    @staticmethod
    def create_connection(db_type: DbType, **kwargs) -> Connection:
        if db_type == DbType.POSTGRES:
            return PostgresConnection(
                protocol=kwargs["protocol"] or "posgresql+psycopg2",
                credential=kwargs["credential"], 
                host=kwargs["host"], 
                port=kwargs["port"], 
                db_name=kwargs["db_name"]
            )
        elif db_type == DbType.SQLITE:
            return SQLiteConnection(db_name=kwargs["db_name"])
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
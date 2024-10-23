from db import DbType, Connection, BaseDatabase
from db.provider.postgres import PostgresDatabase
from db.provider.sqlite import SQLiteDatabase

class Database:

    def __init__(self, db_type: DbType, connection: Connection):
        self.db_type = db_type
        self.connection = connection
        self.database = self._get_database_class()

    def _get_database_class(self):
        match self.db_type:
            case DbType.POSTGRES:
                return PostgresDatabase(self.connection)
            case DbType.SQLITE:
                return SQLiteDatabase(self.connection)
            case _:
                raise ValueError("Unsupported database type")

    def connect(self):
        return self.database.connect()
    
    def get_sql_adapter(self):
        return self.get_sql_adapter()

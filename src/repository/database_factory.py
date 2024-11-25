from repository.db_type import DbType
from repository.connection import Connection
from repository.provider.postgres import PostgresDatabase
from repository.provider.sqlite import SQLiteDatabase


class DatabaseFactory:
    def __init__(self, db_type: DbType, connection: Connection):
        self.db_type = db_type
        self.connection = connection
        self.database = self.__get_database_class()

    def __get_database_class(self):
        match self.db_type:
            case DbType.POSTGRES:
                return PostgresDatabase(self.connection)
            case DbType.SQLITE:
                return SQLiteDatabase(self.connection)
            case _:
                raise ValueError("Unsupported database type")

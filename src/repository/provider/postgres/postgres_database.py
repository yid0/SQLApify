from sqlmodel import create_engine
from repository import BaseDatabase
from .postgres_adapter import PostgresAdapter

class PostgresDatabase(BaseDatabase):
    _instance = None

    def __new__(cls, connection):
        if cls._instance is None:
            cls._instance = super(PostgresDatabase, cls).__new__(cls)
            cls._instance.connection = connection
        return cls._instance

    def connect(self):
        try:
            url = self.get_connection_url()
            self.engine = create_engine(url)
            print(self.engine)
            return self.engine
        except Exception as e:
            raise Exception(f"PostgreSQL Connection Error: {str(e)}")

    def get_connection_url(self) -> str:
        return self.connection.url()
    
    def get_sql_adapter(self) -> PostgresAdapter:
        return PostgresAdapter()

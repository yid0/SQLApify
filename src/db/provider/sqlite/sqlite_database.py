from sqlmodel import create_engine
from db import BaseDatabase

class SQLiteDatabase(BaseDatabase):
    _instance = None

    def __new__(cls, connection):
        if cls._instance is None:
            cls._instance = super(SQLiteDatabase, cls).__new__(cls)
            cls._instance.connection = connection
        return cls._instance

    def connect(self):
        try:
            url = self.get_connection_url()
            self.engine = create_engine(url)
            print("Connected to SQLite database")
            return self.engine
        except Exception as e:
            raise Exception(f"SQLite Connection Error: {str(e)}")

    def get_connection_url(self) -> str:
        return f"sqlite:///{self.connection.db_name}.db"



from db import Connection

class SQLiteConnection(Connection):
    
    def __init__(self, db_name: str):
        self.db_name = db_name

    def url(self) -> str:
        return str(self)
        

    def __str__(self):
        return  f"sqlite:///{self.db_name}.db"

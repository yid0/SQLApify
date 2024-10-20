from db import Connection

class Database:
    type: ("pg")

    db_name: str

    connection: Connection
        
    def __init__(self, type: str, connection: Connection):
        self.type = type
        self.connection = connection


    def connect(self) -> bool :
        try:
            print("Connecting to database")
            return True
        except e :
            raise Exception("Connection Error %s", e) 
        
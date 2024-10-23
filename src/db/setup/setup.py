import os
from enum import Enum
from sqlmodel import Session 
from db import Database, ConnectionFactory, Credential, DbType
from db.query import QueryRole, QueryUser



class Setup:
    _db : Database
    _session: Session
    
    def __init__(self, db_type: DbType):

        protocol, host, port, db_name, username, password = self.load_config()
        credential = Credential(username= username, password= password)
        connection = ConnectionFactory.create_connection(
            db_type= DbType.POSTGRES, 
            protocol= protocol,
            host= host, 
            port= port, 
            db_name= db_name,
            credential= credential
        )        
        self._db = Database(db_type= db_type , connection = connection)

        
    def create_user_app(self):
        
        engine = self._db.connect()
        session = Session(engine)

        sql_adapter = self._db.get_sql_adapter()
        query_role = QueryRole(session, sql_adapter)
        query_user = QueryUser(session, sql_adapter)

        query_role.create_role("management_role")
        
        ## TODO : Add grant privileges 
        query_role.grant_privileges_to_management_role("management_role")

from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from abc import ABC
from repository.database import Database
from repository.connection_factory import ConnectionFactory
from repository.query import QueryRole, QueryDb
from config.configuration import Configuration
from config.app_user_config import ApplicationUserConfig

class DatabaseService(ABC): 
    _instances = {}
    
    def __new__(cls):
        provider = ApplicationUserConfig.get_env(ApplicationUserConfig.APP_BUILD_TARGET.env_name)
        if provider not in cls._instances:
            instance = super(DatabaseService, cls).__new__(cls)
            instance.initialize()
            cls._instances[provider] = instance
        return cls._instances[provider]

    def initialize(self):
        """Init the service by loading DB configurtaions and create the database object"""

        print("initialize : initilize db connection")
        self.app_user_config = Configuration(ApplicationUserConfig)
        self.app_user_config_dict = self.app_user_config.load()
        self.database = Database(
            db_type=ApplicationUserConfig.get_env(ApplicationUserConfig.APP_BUILD_TARGET.env_name),
            connection=ConnectionFactory.create_connection(db_type=ApplicationUserConfig.get_env(ApplicationUserConfig.APP_BUILD_TARGET.env_name), 
                                                           kwargs=self.app_user_config_dict)
        )
    
    def _get_session_and_adapter(self):
        """Get session and database adapter objects as a tuple"""
        engine = self.database.connect()
        session = Session(engine)
        sql_adapter = self.database.get_sql_adapter()
        return session, sql_adapter
  
    async def execute(self, dto):
        """Execute query based on the Data Object Transfer"""

        role_name = self.create_role(role_name=dto.username, password=dto.password)
        return self.create_db(role_name=role_name, db_name=dto.database)


    def create_role(self, role_name: str, password: str) -> Optional[str]:
        """Creates a role in the database with the specified name and password."""
        try:
            session, sql_adapter = self._get_session_and_adapter()
            with session:
                query_role = QueryRole(session, sql_adapter)
                result: bool = query_role.create(role_name, password)
            return role_name if result else None
        except SQLAlchemyError as e:
            print(f"Error creating role {role_name}: {e}")
            return None

    def create_db(self, db_name: str, role_name: str) -> Optional[str]:
        """Creates a database in the DBMS, with the specified role as the owner."""
        try:
            session, sql_adapter = self._get_session_and_adapter()
            with session:
                query_db = QueryDb(session, sql_adapter)
                result = query_db.create(db_name=db_name, owner=role_name)
            return db_name if result else None
        except SQLAlchemyError as e:
            print(f"Error creating database {db_name}: {e}")
            return None

from sqlmodel import Session
from repository import Database, ConnectionFactory, DbType
from repository.query import QueryRole, QueryDb
from config import Configuration
from typing import Optional

class Setup:
    """Setup class for configuring and initializing database components."""
    
    db_type: DbType
    _session: Optional[Session] = None
    _database: Optional[Database] = None

    def __init__(self, db_type: DbType, config: Configuration):     
        """
        Initialize the Setup with the specified database type and configuration.
        
        Args:
            db_type (DbType): The type of the database (e.g., postgres, sqlite).
            config (Configuration): Configuration object with environment settings.
        """
        self.db_type = db_type
        env_config = config.config_type.load(config.config_type)
        connection = ConnectionFactory.create_connection(db_type=db_type, kwargs=env_config)  
        self._database = Database(db_type=db_type, connection=connection)

    def reset_all(self):
        """Reset the database and session attributes."""
        if self._database:
            self._database = None
        if self._session:
            self._session = None
   
    def create_management_role(self, role_name: str, password: str) -> Optional[str]:
        """
        Create a management role in the database with the specified name and password.
        
        Args:
            role_name (str): The name of the role.
            password (str): The password for the role.
        
        Returns:
            Optional[str]: The role name if created successfully, None otherwise.
        """
        if not self._database:
            raise ValueError("Database is not initialized.")
        
        engine = self._database.connect()
        with Session(engine) as session:
            sql_adapter = self._database.get_sql_adapter()
            query_role = QueryRole(session, sql_adapter)
            result: bool = query_role.create(role_name, password)
        return role_name if result else None
    
    def create_management_db(self, db_name: str, role_name: str) -> bool:
        """
        Create a management database with the specified name and assign the role as owner.
        
        Args:
            db_name (str): The name of the database.
            role_name (str): The name of the role that will own the database.
        
        Returns:
            bool: True if the database is created successfully, False otherwise.
        """
        if not self._database:
            raise ValueError("Database is not initialized.")
        
        engine = self._database.connect()
        with Session(engine) as session:
            sql_adapter = self._database.get_sql_adapter()
            query_db = QueryDb(session, sql_adapter)
            result = query_db.create(db_name=db_name, owner=role_name)
        return result                

    def get_database(self) -> Database:
        """
        Get the initialized Database object.
        
        Returns:
            Database: The database instance.
        """
        if not self._database:
            raise ValueError("Database is not initialized.")
        return self._database

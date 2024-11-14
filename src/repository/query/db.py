from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError
from repository import SQLStatementAdapter

class QueryDb:
    """
    Class to handle database-related queries in the database management system.
    """

    def __init__(self, session: Session, adapter: SQLStatementAdapter):
        """
        Initialize QueryDb with a session and SQL statement adapter.
        
        Args:
            session (Session): SQLModel session object.
            adapter (SQLStatementAdapter): Adapter to generate SQL statements.
        """
        self.session = session
        self.adapter = adapter

    def create(self, db_name: str, owner: str) -> bool:
        """
        Create a database in the DBMS with the specified name and owner.
        
        Args:
            db_name (str): The name of the database to create.
            owner (str): The owner of the new database.
        
        Returns:
            bool: True if the database was created successfully, False otherwise.
        """
        try:
            query = self.adapter.create_db_statement(db_name, owner)
            self.session.connection(execution_options={"isolation_level": "AUTOCOMMIT"}).execute(query)
            print(f"Database '{db_name}' was created successfully.")
            return True
        except SQLAlchemyError as e:
            error_message = str(e.__cause__) if e.__cause__ else str(e)
            print(f"ERROR: {error_message}")
            return False
        finally:
            self.session.close()

from sqlmodel import Session
from repository import SQLStatementAdapter
from sqlalchemy.exc import SQLAlchemyError

class QueryUser:
    """
    Class to handle user-related queries in the database.
    """

    def __init__(self, session: Session, adapter: SQLStatementAdapter):
        """
        Initialize QueryUser with a session and SQL statement adapter.
        
        Args:
            session (Session): SQLModel session object.
            adapter (SQLStatementAdapter): Adapter to generate SQL statements.
        """
        self.session = session
        self.adapter = adapter

    def create(self, username: str, password: str):
        """
        Create a user in the database with the specified username and password.
        
        Args:
            username (str): The name of the user.
            password (str): The password for the user.
        
        Raises:
            SQLAlchemyError: If there is an error executing the SQL statement.
        """
        query = self.adapter.create_user_statement(username, password)
        try:
            self.session.exec(query)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error creating user {username}: {e}")
            raise
        finally:
            self.session.close()

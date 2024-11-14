from sqlmodel import Session
from sqlalchemy.exc import ProgrammingError
from repository import SQLStatementAdapter
from .query import Query

class QueryRole(Query):
    """
    Class to handle role-related queries in the database.
    """

    def __init__(self, session: Session, adapter: SQLStatementAdapter):
        """
        Initialize QueryRole with a session and SQL statement adapter.
        
        Args:
            session (Session): SQLModel session object.
            adapter (SQLStatementAdapter): Adapter to generate SQL statements.
        """
        self.session = session
        self.adapter = adapter

    def create(self, role_name: str, password: str) -> bool:
        """
        Create a role in the database with the specified name and password.
        
        Args:
            role_name (str): The name of the role to create.
            password (str): The password for the role.
        
        Returns:
            bool: True if the role was created successfully, False otherwise.
        """
        try:
            query = self.adapter.create_role_statement(role_name, password)
            self.session.exec(query)
            self.session.commit()
            print(f"Role '{role_name}' was created successfully.")
            return True
        except ProgrammingError as e:
            error_message = str(e.__cause__)
            if "exists" in error_message:
                print(f"ERROR: {error_message}")
                return True
            print(f"ProgrammingError: {error_message}")
            return False
        except Exception as e:
            error_message = str(e.__cause__) if e.__cause__ else str(e)
            print(f"ERROR: {error_message}")
            return False
        finally:
            self.session.close()
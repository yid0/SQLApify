from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError
from repository import SQLStatementAdapter


class QuerySchema:
    """
    Class to handle schema-related queries in the database.
    """

    def __init__(self, session: Session, adapter: SQLStatementAdapter):
        """
        Initialize QuerySchema with a session and SQL statement adapter.

        Args:
            session (Session): SQLModel session object.
            adapter (SQLStatementAdapter): Adapter to generate SQL statements.
        """
        self.session = session
        self.adapter = adapter

    def create(self, schema_name: str) -> bool:
        """
        Create a schema in the database with the specified name.

        Args:
            schema_name (str): The name of the schema to create.

        Returns:
            bool: True if the schema was created successfully, False otherwise.
        """
        try:
            query = self.adapter.create_schema_statement(schema_name)
            self.session.exec(query)
            self.session.commit()
            print(f"Schema '{schema_name}' was created successfully.")
            return True
        except SQLAlchemyError as e:
            print(f"Error creating schema '{schema_name}': {e}")
            self.session.rollback()
            return False
        finally:
            self.engine.dispose()

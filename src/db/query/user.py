from sqlmodel import Session
from db import SQLStatementAdapter

class QueryUser:
    def __init__(self, session: Session, adapter: SQLStatementAdapter):
        self.session = session
        self.adapter = adapter

    def create_user(self, username: str, password: str):
        query = self.adapter.create_user_statement(username, password)
        self.session.execute(query)
        self.session.commit()
        self.session.close()

        print(f"Utilisateur {username} créé avec succès.")

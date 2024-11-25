from abc import ABC


class BaseService(ABC):
    def _get_session_and_adapter(self):
        """Get session and database adapter objects as a tuple"""
        session = self.database.connect()
        sql_adapter = self.database.get_sql_adapter()
        return session, sql_adapter

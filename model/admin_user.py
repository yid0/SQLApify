from typing import Optional

from sqlmodel import Field, SQLModel

class AdminUser(SQLModel, table=True):
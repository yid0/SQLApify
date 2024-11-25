from pydantic import BaseModel, Field, validator
from typing import List, Optional
from common import SQLObjectType, SQLPrivilegeType


## TODO: finalize data object definition
class CreateUserRoleDTO(BaseModel):
    provider: str = Field(
        default="default",
        defadescription="Database engine targeted to execute the query",
    )
    username: str = Field(description="Name of the role to be created")
    password: str = Field(description="Password for the role")
    schema: bool = Field(
        None, description="Set to true if the database engine supports schemas"
    )
    database: str = Field(description="Name of the user's database to be created")
    privileges: List[SQLPrivilegeType] = Field(
        None, init_var=[], description="List of privileges to assign"
    )
    object_type: SQLObjectType = Field(
        None, init_var="VIEW", description="Type of database object (e.g., TABLE, VIEW)"
    )
    object_name: str = Field(
        None,
        description="Full object name, including schema if applicable (e.g., schema.table_name)",
    )
    grantee: Optional[str] = Field(
        None,
        validate_default=False,
        description="Role name to which the privileges are assigned",
    )

    @validator("object_name")
    def validate_object_name(cls, value):
        if cls.schema and "." not in value:
            raise ValueError(
                "The object must be specified with a schema (e.g., schema.table_name)"
            )
        return value

from pydantic import BaseModel, field_validator
import re


class BaseValidator(BaseModel):
    @field_validator(
        "protocol",
        "username",
        "password",
        "host",
        "port",
        "schema",
        "database",
        check_fields=False,
    )
    def validate_not_empty(cls, value):
        if not value:
            raise ValueError(f"Property cannot be empty, given value: {value}")
        return value

    @field_validator("password", check_fields=False)
    def validate_password(cls, value):
        # if not re.search(r"[A-Za-z]", value) or not re.search(r"[0-9]", value):
        #     raise ValueError("The password must contain at least one letter and one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("The password must contain a special character.")
        return value

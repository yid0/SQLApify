from pydantic import BaseModel


class BaseResponse(BaseModel):
    status_code: int = 200
    message: str = "Resource created or updated successfully."
    detail: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

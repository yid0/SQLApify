from pydantic import BaseModel

class BaseResponse(BaseModel):
    status_code: int = 201
    message: str = "Resource created."
    
    def __init__(self, message: str, status_code: int, **kwargs):
        super().__init__(**kwargs)
        self.status_code = status_code
        self.message = message
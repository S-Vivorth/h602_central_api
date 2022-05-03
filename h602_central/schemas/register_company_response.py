
from pydantic import BaseModel

class register_company_response(BaseModel):
    message: str
    code: str
    data: dict
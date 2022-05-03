
from pydantic import BaseModel

class modify_bank_status_response(BaseModel):
    message: str
    code: str
    data: dict
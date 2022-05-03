
from pydantic import BaseModel

class operations_add_bank_response(BaseModel):
    message: str
    code: str
    data: list
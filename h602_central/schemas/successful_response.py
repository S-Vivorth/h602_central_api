
from pydantic import BaseModel

class successful_response(BaseModel):
    message: str = 'success'
    code: str = '000'
    data: list = []
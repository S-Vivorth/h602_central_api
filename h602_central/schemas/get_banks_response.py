

from pydantic import BaseModel
from typing import List

class bank(BaseModel):
    code: str
    logo: str
    name: str
    id: str

class get_banks_response(BaseModel):
    message: str
    code: str
    data: List[bank]



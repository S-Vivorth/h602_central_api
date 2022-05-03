from pydantic import BaseModel
from typing import List

class banks(BaseModel):
    bank_id: str

class operations_add_bank_request(BaseModel):
    company_id: int
    banks: List[banks]

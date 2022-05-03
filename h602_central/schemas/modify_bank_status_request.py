
from pydantic import BaseModel

class modify_bank_status_request(BaseModel):
    company_id: int
    company_b24_id: int
    bank_id: str
    status: int
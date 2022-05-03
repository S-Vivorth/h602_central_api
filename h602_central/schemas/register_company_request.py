from pydantic import BaseModel
from typing import List


class billers(BaseModel):
    b24_biller_code: str
    b24_token: str
    currency: list
    ar_accounts: list

class register_company_request(BaseModel):
    register_id: int

    billers: List[billers]

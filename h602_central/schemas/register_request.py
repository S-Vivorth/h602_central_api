
from pydantic import BaseModel
from typing import List

class banks(BaseModel):
    bank_id: str
    bank_name: str
class register_request(BaseModel):
    company_name_kh: str
    company_name_eng: str
    phone: str
    email: str
    tin_number: str
    address_kh: str = ''
    address_eng: str = ''
    banks: List[banks]
    file_document: str
    ar_accounts: list


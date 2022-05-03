
from pydantic import BaseModel


class pull_invoices_request(BaseModel):
    d1: str = '2022-02-01'
    d2: str = '2022-02-10'
    b24_biller_code: str
from pydantic import BaseModel
from typing import List


class bills(BaseModel):
    code: str
    org_code: str
    sync_code: str
    customer_code: str
    total_amount: float
    pay_amount: float


class data(BaseModel):
    id: str
    code: str
    title: str
    tran_date: str
    payment_type: str
    payment_method: str = ''
    tran_amount: float
    fee_amount: float
    total_amount: float
    supplier_fee: float
    currency_id: str
    customer_sync_code: str
    customer_org_code: str
    customer_name: str
    payment_ref: str
    bank_id: str
    bank_name: str
    bills: List[bills]


class pull_invoices_response(BaseModel):
    message: str
    code: str
    data: data

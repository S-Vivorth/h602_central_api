from pydantic import BaseModel
from datetime import datetime
from typing import List
class ext_details(BaseModel):
    id: str
    txn_line_id: str
    txn_invoice_id: str
    item_list_id: str
    item_name: str
    description: str
    quantity: float
    price: float
    amount: float
    class_list_id: str
    sales_tax_code_list_id: str
class invoice_push_request(BaseModel):
    txn_id: str
    b24_biller_code: str
    company_id: int
    ref_number: str
    txn_date: datetime
    due_date: datetime
    customer_list_id: str
    customer_name: str
    exchange_rate: float
    total_amount: float
    bill_type: int
    status: str
    bill_address: str = ''
    ship_address: str = ''
    memo: str = ''
    is_pending: bool = True
    po_number: str = ''
    fob: str = ''
    ship_date: datetime = datetime.now()
    currency_list_id: str
    currency_name: str
    sales_rep_list_id: str
    ship_method_list_id: str
    ar_account_ref_list_id: str
    template_ref_list_id: str
    terms_ref_list_id: str
    item_sales_tax_ref_list_id: str
    class_ref_list_id: str
    ext_details: List[ext_details]




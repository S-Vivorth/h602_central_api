from pydantic import BaseModel

class invoices_push_response(BaseModel):
    message: str
    code: str
    data: dict
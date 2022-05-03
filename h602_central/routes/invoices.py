from fastapi import APIRouter, Header, Request
from typing import List

from h602_central.logics import invoices_logics
from h602_central.schemas.invoice_push_request import invoice_push_request
invoices = APIRouter(prefix='/online_payments', tags=['online_payments'])


@invoices.post('/invoices/push')
def push(payload: List[invoice_push_request], request: Request, token: str = Header(None), qe_token: str = Header(None, convert_underscores=False)):
    return invoices_logics.default.push(payload, request)



from fastapi import APIRouter, Header, Request, Query
from h602_central.schemas.register_request import register_request
from h602_central.schemas.pull_invoices_request import pull_invoices_request
from h602_central.logics import online_payments_logics
from h602_central.schemas.register_response import register_response
from h602_central.schemas.get_banks_response import get_banks_response
from h602_central.schemas.get_queue_status_request import get_queue_status_request
from typing import List
from h602_central.schemas.paging_response import paging_response
online_payments = APIRouter(prefix='/online_payments', tags=['online_payments'])


@online_payments.post('/register', response_model=register_response)
async def register(payload: register_request, request: Request, token: str = Header(None),
                   qe_token: str = Header(None, convert_underscores=False)):
    return await online_payments_logics.default.register(payload, request)


@online_payments.post('/payments/pull')
async def pull(request: Request, payload: pull_invoices_request, token: str = Header(None),
               qe_token: str = Header(None, convert_underscores=False)):
    return await online_payments_logics.default.pull(payload, request)


@online_payments.post('/bank/add')
async def add_bank(payload: register_request, request: Request, token: str = Header(None),
                   qe_token: str = Header(None, convert_underscores=False)):
    return await online_payments_logics.default.add_bank(payload, request)


@online_payments.get('/bank/status')
async def get_bank_status(request: Request, token: str = Header(None),
                          qe_token: str = Header(None, convert_underscores=False)):
    return await online_payments_logics.default.get_bank_status(request=request)


@online_payments.get('/invoices', response_model=paging_response)
async def get_invoices(request: Request, token: str = Header(None),
                       qe_token: str = Header(None, convert_underscores=False), b24_biller_code: str = None,
                        txn_id: str = None, ref_number: str = None, d1: str = None, d2: str = None,
                       per_page: int = None, page: int = None
                       ):
    return await online_payments_logics.default.get_invoices(request=request)


@online_payments.get('/payments')
async def get_payments(request: Request, token: str = Header(None),
                       qe_token: str = Header(None, convert_underscores=False),
                       customer_sync: str = None, d1: str = None, d2: str = None, b24_biller_code: str = None,
                       per_page: int = None, page: int = None):
    return await online_payments_logics.default.get_payments(request=request)


@online_payments.get('/banks', response_model=get_banks_response)
async def get_banks(request: Request, token: str = Header(None),
                    qe_token: str = Header(None, convert_underscores=False)):
    return await online_payments_logics.default.get_banks(request=request)


@online_payments.post('/queue/status')
async def get_queue_status(payload: List[get_queue_status_request],request: Request, token: str = Header(None),
                    qe_token: str = Header(None, convert_underscores=False)):
    return await online_payments_logics.default.get_queue_status(payload=payload, request=request)
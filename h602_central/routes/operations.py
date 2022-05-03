from fastapi import APIRouter, Header, Request
from h602_central.schemas.register_company_request import register_company_request
from h602_central.logics import operations_logics
from h602_central.schemas.operations_add_bank_request import operations_add_bank_request
from h602_central.schemas.add_more_billers import add_more_billers
from h602_central.schemas.modify_bank_status_request import modify_bank_status_request
operations = APIRouter(prefix='/operations', tags=['operations'])


@operations.post('/registercompany')
async def register_company(payload: register_company_request, request: Request, token: str = Header(None)):
    return await operations_logics.default.register_company(payload, request)


@operations.post('/bank/add')
async def add_bank(payload: operations_add_bank_request, request: Request, token: str = Header(None)):
    return await operations_logics.default.add_bank(payload, request)


@operations.post('/registercompany/add')
async def add_more_billers(payload: add_more_billers, request: Request, token: str = Header(None)):
    return await operations_logics.default.add_more_billers(payload, request)

@operations.post('/bank/status/modify')
async def modify_bank_status(payload: modify_bank_status_request, request: Request, token: str = Header(None)):
    return await operations_logics.default.modify_bank_status(payload, request)



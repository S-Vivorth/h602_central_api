from h602_central.schemas.register_company_request import register_company_request
from fastapi import Request, HTTPException
from h602_central.logics.settings_logic import settings_logic, db
from fastapi_sqlalchemy import db
from h602_central.models.h602_central_models import *
from h602_central.schemas.register_company_response import register_company_response
from h602_central.schemas.operations_add_bank_request import operations_add_bank_request
from h602_central.schemas.operations_add_bank_response import operations_add_bank_response
from h602_central.schemas.add_more_billers import add_more_billers
from h602_central.logics.base_logics import base_logics
from h602_central.schemas.modify_bank_status_request import modify_bank_status_request
from h602_central.schemas.modify_bank_status_response import modify_bank_status_response


class operations_logics:
    async def register_company(payload: register_company_request, request: Request):
        base_logics.validate_support_token(request=request)
        billers_list = payload.billers

        obj = db.session.query(register_model).filter(register_model.id == payload.register_id,
                                                      register_model.is_active == 't').first()
        if obj is not None:
            company = company_model()
            company.company_name_kh = obj.company_name_kh
            company.company_name = obj.company_name
            company.phone = obj.phone
            company.email = obj.email
            company.tin_number = obj.tin_number
            company.address_kh = obj.address_kh
            company.address = obj.address_kh
            db.session.add(company)
            db.session.commit()

            company_authorize = company_authorize_model()
            company_authorize.company_id = company.id
            company_authorize.qe_token = obj.qe_token
            db.session.add(company_authorize)
            db.session.commit()
            banks_list = obj.banks
            banks_list = list(eval(banks_list))
            for biller in billers_list:
                company_b24 = company_b24_model()
                company_b24.code = biller.b24_biller_code
                company_b24.token = biller.b24_token
                company_b24.company_id = company.id
                company_b24.currency = str(biller.currency)
                company_b24.ar_account = str(biller.ar_accounts)
                db.session.add(company_b24)
                db.session.commit()
                for bank in banks_list:
                    company_b24_bank_status = company_b24_bank_status_model()
                    company_b24_bank_status.company_b24_id = company_b24.id
                    company_b24_bank_status.bank_id = bank["bank_id"]
                    company_b24_bank_status.status = obj.status
                    db.session.add(company_b24_bank_status)
                    db.session.commit()

            return register_company_response(
                message='success',
                code='000',
                data={
                    "company_name_kh": obj.company_name_kh, "company_name": obj.company_name_kh,
                    "phone": obj.phone,
                    "email": obj.email, "tin_number": obj.tin_number, "address_kh": obj.address_kh,
                    "address": obj.address_kh, "banks": banks_list,
                    "b24_billers": billers_list}
            )
        else:
            raise HTTPException(status_code=404, detail={
                "message": "Invalid register_id ",
                "code": "404",
                "data": {}
            })

    async def add_bank(payload: operations_add_bank_request, request: Request):
        base_logics.validate_support_token(request=request)
        obj = db.session.query(company_model).filter(company_model.id == payload.company_id,
                                                     company_model.is_active == 't').first()

        if obj is not None:
            company_b24_obj_list = db.session.query(company_b24_model).filter(
                company_b24_model.company_id == payload.company_id, company_b24_model.is_active == 't').all()
            company_b24_id_list = []
            for company_b24 in company_b24_obj_list:
                company_b24_id_list.append(company_b24.id)
            banks_list = payload.banks
            company_b24_id_list.sort()
            data = []
            for company_b24_id in company_b24_id_list:
                for bank in banks_list:
                    company_b24_bank_status = company_b24_bank_status_model()
                    company_b24_bank_status.company_b24_id = company_b24_id
                    company_b24_bank_status.bank_id = bank.bank_id
                    company_b24_bank_status.status = 1
                    data.append({"company_b24_id": company_b24_id, "bank_id": bank.bank_id, "status": 1})
                    db.session.add(company_b24_bank_status)
                db.session.commit()

            return operations_add_bank_response(
                message='success',
                code='000',
                data=data
            )
        else:
            raise HTTPException(status_code=404, detail={
                "message": "Invalid company_id",
                "code": "404",
                "data": {}
            })

    async def add_more_billers(payload: add_more_billers, request: Request):
        billers_list = payload.billers

        base_logics.validate_support_token(request=request)
        obj = db.session.query(company_model).filter(company_model.id == payload.company_id,
                                                     company_model.is_active == 't').first()
        if obj is not None:

            company_b24_obj = db.session.query(company_b24_model).filter(
                company_b24_model.company_id == payload.company_id,
                company_b24_model.is_active == 't').first()

            company_b24_id = company_b24_obj.id
            company_b24_bank_status_model_obj_list = db.session.query(company_b24_bank_status_model).filter(
                company_b24_bank_status_model.company_b24_id == company_b24_id,
                company_b24_bank_status_model.is_active == 't').all()
            bank_id_list = []
            for company_b24_bank_status_model_obj in company_b24_bank_status_model_obj_list:
                bank_id_list.append(company_b24_bank_status_model_obj.bank_id)
            for biller in billers_list:
                company_b24 = company_b24_model()
                company_b24.code = biller.b24_biller_code
                company_b24.token = biller.b24_token
                company_b24.currency = str(biller.currency)
                company_b24.ar_account = str(biller.ar_accounts)
                company_b24.company_id = payload.company_id
                db.session.add(company_b24)
                db.session.commit()
                for bank_id in bank_id_list:
                    company_b24_bank_status = company_b24_bank_status_model()
                    company_b24_bank_status.company_b24_id = company_b24.id
                    company_b24_bank_status.bank_id = bank_id
                    company_b24_bank_status.status = 1
                    db.session.add(company_b24_bank_status)
                db.session.commit()

            return {
                "message": "success",
                "code": "000",
                "data": {
                    "company_name": obj.company_name,
                    "company_name_kh": obj.company_name_kh,
                    "phone": obj.phone,
                    "email": obj.email,
                    "tin_number": obj.tin_number,
                    "address": obj.address,
                    "address_kh": obj.address_kh,
                    "b24_billers": billers_list
                }
            }
        else:
            raise HTTPException(status_code=403, detail={
                "message": "Invalid company_id",
                "code": "403",
                "data": {}
            })

    async def modify_bank_status(payload: modify_bank_status_request, request: Request):
        base_logics.validate_support_token(request=request)
        obj = db.session.query(company_model).filter(company_model.id == payload.company_id,
                                                     company_model.is_active == 't').first()
        if obj is not None:
            company_b24_obj = db.session.query(company_b24_model).filter(
                company_b24_model.id == payload.company_b24_id,
                company_b24_model.is_active == 't').first()

            if company_b24_obj is not None:
                bank = db.session.query(bank_model).filter(bank_model.id == payload.bank_id,
                                                           bank_model.is_actove == 't').first()
                if bank is not None:
                    company_b24_bank_status = db.session.query(company_b24_bank_status_model).filter(
                        company_b24_bank_status_model.company_b24_id == payload.company_b24_id,
                        company_b24_bank_status_model.bank_id == payload.bank_id,
                        company_b24_bank_status_model.is_active == 't'
                    ).first()

                    new_company_b24_bank_status = company_b24_bank_status_model()
                    new_company_b24_bank_status.status = 2

                    base_logics.copy(new_company_b24_bank_status, company_b24_bank_status,
                                     ignores=['id', 'is_active', 'created_date', 'updated_date', 'updated_by',
                                              'created_by',
                                              'company_b24_id', 'bank_id'])
                    if company_b24_bank_status is not None:
                        return modify_bank_status_response(
                            message='success',
                            code='000',
                            data={
                                "company_b24_id": payload.company_b24_id,
                                "bank_id": payload.bank_id,
                                "status": payload.status
                            }
                        )
                    else:
                        base_logics.raise_exception(409, "Invalid company_b24_bank_status")
                else:
                    base_logics.raise_exception(406, "Invalid bank_id")
            else:
                base_logics.raise_exception(408, "Invalid company_b24_id")

        else:
            base_logics.raise_exception(403, "Invalid company_id")


default = operations_logics

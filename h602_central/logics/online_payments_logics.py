import json

from h602_central.schemas.register_request import register_request
from h602_central.schemas.register_response import register_response
from h602_central.schemas.pull_invoices_request import pull_invoices_request
from h602_central.schemas.pull_invoices_response import pull_invoices_response
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from h602_central.logics.settings_logic import settings_logic, db
from fastapi import Request, HTTPException
from h602_central.models.h602_central_models import *
from h602_central.logics import jwt_logic
from h602_central.logics.base_logics import base_logics
import datetime
from h602_central.schemas.get_banks_response import get_banks_response
from h602_central.schemas.get_queue_status_request import get_queue_status_request
from typing import List
from h602_central.schemas.get_queue_status_response import get_queue_status_response
from h602_central.schemas.paging_response import paging_response
from sqlalchemy.orm import defer
from h602_central.schemas.successful_response import successful_response

class online_payments_logics:
    async def register(self, payload: register_request, request: Request):
        token = request.headers.get('token')
        qe_token = request.headers.get('qe_token')
        base_logics.validate_tokens(token, qe_token)
        bank_list_string = []
        banks = []
        banks_list = payload.banks
        register = register_model()
        register.company_name_kh = payload.company_name_kh
        register.company_name = payload.company_name_eng
        register.phone = payload.phone
        register.email = payload.email
        register.tin_number = payload.tin_number
        register.address_kh = payload.address_kh
        register.address = payload.address_eng
        register.file_document = payload.file_document
        for bank in banks_list:
            banks.append(bank.bank_name)
            bank_list_string.append({"bank_id": bank.bank_id, "bank_name": bank.bank_name})
        ar_accounts = ', '.join(payload.ar_accounts)
        register.banks = str(bank_list_string)
        register.status = 1
        register.qe_token = qe_token
        db.session.add(register)
        db.session.commit()

        banks = ', '.join(banks)
        body = """
                     Dear Support Team,<br>
                                        <br>
                                        There is a new online payment request on QE as following:<br>
                                        <br>
                                        - Company name in KH: <b>%s</b> <br>
                                        - Company name in EN: <b>%s</b> <br>
                                        - Phone Number: <b> %s </b> <br>
                                        - Email: <b> %s </b> <br>
                                        - TIN Number: <b> %s </b> <br>
                                        - Address in KH: <b> %s </b> <br>
                                        - Address in EN: <b> %s </b> <br>
                                        - Bank Name: <b>%s</b> <br>
                                        - Request Id: %s <br>
                                        - ar_accounts: %s <br>
                                        <br>
                                        kindly process to activate. <br>
                                        <br>
                                        Thank you.
                    """ % (payload.company_name_kh, payload.company_name_eng, payload.phone,
                           payload.email, payload.tin_number, payload.address_kh, payload.address_eng, banks,
                           register.id, ar_accounts)

        await send_mail(subject="[QE] New Online Payment Request ", body=body)
        return register_response(
            message='success',
            code='000',
            data=payload
        )

    async def pull(self, payload: pull_invoices_request, request: Request):
        try:
            d1 = datetime.datetime.strptime(payload.d1, '%Y-%m-%d')
            d2 = datetime.datetime.strptime(payload.d2, '%Y-%m-%d')
        except:
            raise HTTPException(406, detail={
                "message": 'Incorrect date format',
                "code": "406",
                "data": {}
            })

        token = request.headers.get('token')
        qe_token = request.headers.get('qe_token')
        base_logics.validate_tokens(token, qe_token)
        company_id = get_company_id(qe_token=qe_token)
        if company_id is not None:
            receive_payments = db.session.query(receive_payment_model).options(defer('updated_by'),
                                                                               defer('updated_date'),
                                                                               defer('created_by'),
                                                                               defer('created_date'),
                                                                               defer('is_active')).filter(
                receive_payment_model.b24_biller_code == payload.b24_biller_code,
                receive_payment_model.is_active == 't',
                receive_payment_model.paid_date >= d1,
                receive_payment_model.paid_date <= d2
            ).all()
            if receive_payments:
                return successful_response(
                    data=receive_payments
                )
            else:
                return successful_response()



    async def add_bank(self, payload: register_request, request: Request):
        token = request.headers.get('token')
        qe_token = request.headers.get('qe_token')
        base_logics.validate_tokens(token, qe_token)
        company_id = get_company_id(qe_token=qe_token)
        banks = []
        banks_list = payload.banks
        for bank in banks_list:
            banks.append(bank.bank_name)
        banks = ', '.join(banks)

        body = """
                             Dear Support Team,<br>
                                                <br>
                                                There is a request on QE for activate new banks as following:<br>
                                                <br>
                                                - Company name in KH: <b>%s</b> <br>
                                                - Company name in EN: <b>%s</b> <br>
                                                - Company id: <b>%s</b> <br>
                                                - Phone Number: <b> %s </b> <br>
                                                - Email: <b> %s </b> <br>
                                                - TIN Number: <b> %s </b> <br>
                                                - Address in KH: <b> %s </b> <br>
                                                - Address in EN: <b> %s </b> <br>
                                                - Bank Name: <b>%s</b> <br>
                                                <br>
                                                kindly process to activate. <br>
                                                <br>
                                                Thank you.
                            """ % (payload.company_name_kh, payload.company_name_eng, company_id, payload.phone,
                                   payload.email, payload.tin_number, payload.address_kh, payload.address_eng, banks
                                   )
        await send_mail(subject="[QE] New Banks Activation Request", body=body)
        return register_response(
            message='success',
            code='000',
            data=payload
        )

    async def get_bank_status(self, request: Request):
        token = request.headers.get('token')
        qe_token = request.headers.get('qe_token')
        base_logics.validate_tokens(token, qe_token)

        company_id = get_company_id(qe_token)
        company_b24_list = db.session.query(company_b24_model).filter(
            company_b24_model.company_id == company_id, company_b24_model.is_active == 't'
        ).all()
        company_b24_id_list = []
        company_b24_code_list = []
        for company_b24 in company_b24_list:
            company_b24_id_list.append(company_b24.id)
            company_b24_code_list.append(company_b24.code)
        data = []
        for company_b24_id in company_b24_id_list:
            company_b24_bank_status_list = db.session.query(company_b24_bank_status_model).filter(
                company_b24_bank_status_model.company_b24_id == company_b24_id,
                company_b24_bank_status_model.is_active == 't'
            ).all()
            index = 0
            for company_b24_bank_status in company_b24_bank_status_list:
                data.append(
                    {"b24_biller_code": company_b24_code_list[index], "bank_id": company_b24_bank_status.bank_id,
                     "status": company_b24_bank_status.status})
            index = index + 1
        return {
            "message": "success",
            "code": "000",
            "data": data
        }

    async def get_banks(self, request: Request):
        token = request.headers.get('token')
        qe_token = request.headers.get('qe_token')
        base_logics.validate_tokens(token, qe_token)

        obj = db.session.query(company_authorize_model).filter(company_authorize_model.qe_token == qe_token,
                                                               company_authorize_model.is_active == 't').first()
        if obj is not None:
            banks_list_obj = db.session.query(bank_model).filter(bank_model.is_active == 't').all()
            banks_list = []
            for bank in banks_list_obj:
                banks_list.append({"code": bank.code, "id": bank.id, "logo": bank.logo, "name": bank.name})
            return get_banks_response(
                message='success',
                code='000',
                data=banks_list
            )
        else:
            raise HTTPException(status_code=401, detail={
                "message": "Unauthorized",
                "code": "401",
                "data": {}
            })

    async def get_queue_status(self, payload: List[get_queue_status_request], request: Request):
        token = request.headers.get('token')
        qe_token = request.headers.get('qe_token')
        base_logics.validate_tokens(token, qe_token)
        obj = db.session.query(company_authorize_model).filter(company_authorize_model.qe_token == qe_token,
                                                               company_authorize_model.is_active == 't').first()
        if obj is not None:
            response_list = []
            for item in payload:
                print(item)
                queue = db.session.query(queue_model).filter(queue_model.id == item.queue_id,
                                                             queue_model.is_active == 't').first()
                if queue is not None:
                    queue_detail = db.session.query(queue_detail_model).filter(
                        queue_detail_model.queue_id == item.queue_id, queue_detail_model.is_active == 't'
                    ).first()

                    response_list.append(
                        get_queue_status_response(
                            status=queue.status,
                            total_record=queue.total_record,
                            type=queue.type,
                            data=queue_detail.data
                        )
                    )
            return response_list

    async def get_invoices(self, request: Request):
        token = request.headers.get('token')
        qe_token = request.headers.get('qe_token')
        base_logics.validate_tokens(token, qe_token)
        obj = db.session.query(company_authorize_model).filter(company_authorize_model.qe_token == qe_token,
                                                               company_authorize_model.is_active == 't').first()
        if obj is not None:
            b24_biller_code = request.query_params.get('b24_biller_code')
            b24_biller_code = list(map(str, eval(b24_biller_code)))
            txn_id = request.query_params.get('txn_id')
            ref_number = request.query_params.get('ref_number')
            current_page = request.query_params.get('page')
            per_page = request.query_params.get('per_page')
            try:
                datetime.datetime.strptime(request.query_params.get('d1'), '%Y-%m-%d')
                datetime.datetime.strptime(request.query_params.get('d2'), '%Y-%m-%d')

            except:
                raise HTTPException(406, detail={
                    "message": 'Incorrect date format',
                    "code": "406",
                    "data": {}
                })

            d1 = request.query_params.get('d1')
            d2 = request.query_params.get('d2')
            invoices_list = []

            invoices = db.session.query(invoice_model).filter(
                invoice_model.b24_biller_code.in_(b24_biller_code),
                invoice_model.ref_number == ref_number,
                invoice_model.txn_date >= d1,
                invoice_model.txn_date <= d2
            ).order_by(invoice_model.id.asc()).limit(per_page).offset((int(current_page) - 1) * int(per_page)).all()
            total_records = db.session.query(invoice_model).filter(
                invoice_model.b24_biller_code.in_(b24_biller_code),
                invoice_model.ref_number == ref_number,
                invoice_model.txn_date >= d1,
                invoice_model.txn_date <= d2).count()
            if invoices:
                print(len(invoices))
                for invoice in invoices:
                    invoice_details = db.session.query(invoice_detail_model).filter(
                        invoice_detail_model.txn_invoice_id == invoice.txn_id,
                        invoice_detail_model.is_active == 't'
                    ).all()
                    if invoice_details:
                        setattr(invoice, 'ext_details', invoice_details)
                        print(invoice)
                        invoices_list.append(
                            invoice
                        )
                    else:
                        invoices_list.append(invoice)
            return paging_response(
                message='success',
                code='000',
                paging={
                    "per_page": per_page,
                    "total_records": total_records,
                    "page": current_page
                },
                data=invoices_list

            )

    async def get_payments(self, request: Request):
        token = request.headers.get('token')
        qe_token = request.headers.get('qe_token')
        base_logics.validate_tokens(token, qe_token)
        obj = db.session.query(company_authorize_model).filter(company_authorize_model.qe_token == qe_token,
                                                               company_authorize_model.is_active == 't').first()
        if obj is not None:
            customer_sync = request.query_params.get('customer_sync')
            b24_biller_code = request.query_params.get('b24_biller_code')
            b24_biller_code = list(map(str, eval(b24_biller_code)))

            per_page = request.query_params.get('per_page')
            current_page = request.query_params.get('page')
            customer_sync = request.query_params.get('customer_sync')
            customer_sync = request.query_params.get('customer_sync')
            d1 = request.query_params.get('d1')
            d2 = request.query_params.get('d2')
            try:
                d1 = datetime.datetime.strptime(d1, '%Y-%m-%d')
                d2 = datetime.datetime.strptime(d2, '%Y-%m-%d')

            except:
                raise HTTPException(406, detail={
                    "message": 'Incorrect date format',
                    "code": "406",
                    "data": {}
                })

            receive_payments = db.session.query(receive_payment_model).filter(
                receive_payment_model.b24_biller_code.in_(b24_biller_code),
                receive_payment_model.customer_sync_code == customer_sync,
                receive_payment_model.paid_date >= d1,
                receive_payment_model.paid_date <= d2,
                receive_payment_model.is_active == 't'
            ).order_by(receive_payment_model.id.asc()).limit(per_page).offset((int(current_page) - 1) * int(per_page)).all()
            total_records = db.session.query(receive_payment_model).filter(
                receive_payment_model.b24_biller_code.in_(b24_biller_code),
                receive_payment_model.customer_sync_code == customer_sync,
                receive_payment_model.paid_date >= d1,
                receive_payment_model.paid_date <= d2,
                receive_payment_model.is_active == 't'
            ).count()
            if receive_payments:
                return paging_response(
                    paging={
                        "per_page": per_page,
                        "total_records": total_records,
                        "page": current_page
                    },
                    data=receive_payments
                )

def get_company_id(qe_token: str):
    obj = db.session.query(company_authorize_model).filter(company_authorize_model.qe_token == qe_token).first()
    if not obj:
        raise HTTPException(status_code=401, detail={
            "message": "Unauthorized",
            "code": "401",
            "data": {}
        })
    else:
        return obj.company_id


async def send_mail(subject: str, body: str):
    mail_server = settings_logic.get('mail_server')
    mail_port = settings_logic.get('mail_port')
    mail_username = settings_logic.get('mail_username')
    mail_password = settings_logic.get('mail_password')
    mail_default_sender = settings_logic.get('mail_default_sender')
    mail_use_tls = settings_logic.get('mail_use_tls')
    mail_use_ssl = settings_logic.get('mail_use_ssl')
    recipients = settings_logic.get('support_email')

    conf = ConnectionConfig(
        MAIL_USERNAME=mail_username,
        MAIL_PASSWORD=mail_password,
        MAIL_FROM=mail_default_sender,
        MAIL_PORT=mail_port,
        MAIL_SERVER=mail_server,
        MAIL_TLS=mail_use_tls,
        MAIL_SSL=mail_use_ssl,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=False
    )

    message = MessageSchema(
        subject=subject,
        recipients=[recipients],  # List of recipients, as many as you can pass
        html=body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)


default = online_payments_logics()

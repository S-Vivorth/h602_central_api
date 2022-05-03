from h602_central.schemas.invoice_push_request import invoice_push_request
from h602_central.schemas.queue_response import queue_response
from typing import List
from fastapi import Request, HTTPException
from h602_central.logics.settings_logic import settings_logic, db
from h602_central.logics.base_logics import base_logics
from h602_central.models.h602_central_models import *
from datetime import datetime
import requests
import json
from h602_central.schemas.invoices_push_response import invoices_push_response


class invoices_logics:
    @staticmethod
    def push(payload: List[invoice_push_request], request: Request):
        token = request.headers.get('token')
        qe_token = request.headers.get('qe_token')
        base_logics.validate_tokens(token=token, qe_token=qe_token)

        obj = db.session.query(company_authorize_model).filter(company_authorize_model.qe_token == qe_token,
                                                               company_authorize_model.is_active == 't').first()
        if obj is not None:
            queue = queue_model()
            queue.company_id = payload[0].company_id
            queue.date = datetime.now()
            queue.type = 1
            queue.total_record = len(payload)
            data = []
            b24_biller_code_list = []
            for item in payload:
                if b24_biller_code_list.__contains__(item.b24_biller_code) == False:
                    b24_biller_code_list.append(item.b24_biller_code)
                item.due_date = str(item.due_date)
                item.txn_date = str(item.txn_date)
                item.ship_date = str(item.ship_date)
                for index in range(0, len(item.ext_details)):
                    item.ext_details[index] = item.ext_details[index].__dict__
                    print(item.ext_details[index])
                data.append(item.__dict__)
                print(data)
                invoice = db.session.query(invoice_model).filter(invoice_model.txn_id == item.txn_id,
                                                                 invoice_model.is_active == 't').first()
                each_invoice = invoice_model()
                each_invoice.b24_biller_code = item.b24_biller_code
                each_invoice.company_id = item.company_id
                each_invoice.txn_id = item.txn_id
                each_invoice.ref_number = item.ref_number
                each_invoice.txn_date = item.txn_date
                each_invoice.due_date = item.due_date
                each_invoice.customer_list_id = item.customer_list_id
                each_invoice.customer_name = item.customer_name
                each_invoice.exchange_rate = item.exchange_rate
                each_invoice.currency_list_id = item.currency_list_id
                each_invoice.currency_name = item.currency_name
                each_invoice.bill_type = item.bill_type
                each_invoice.status = item.status
                each_invoice.total_amount = item.total_amount
                each_invoice.bill_address = item.bill_address
                each_invoice.ship_address = item.ship_address
                each_invoice.memo = item.memo
                each_invoice.is_pending = item.is_pending
                each_invoice.po_number = item.po_number
                each_invoice.fob = item.fob
                each_invoice.ship_date = item.ship_date
                each_invoice.sales_rep_list_id = item.sales_rep_list_id
                each_invoice.ship_method_list_id = item.ship_method_list_id
                each_invoice.ar_account_ref_list_id = item.ar_account_ref_list_id
                each_invoice.template_ref_list_id = item.template_ref_list_id
                each_invoice.terms_ref_list_id = item.terms_ref_list_id
                each_invoice.item_sales_tax_ref_list_id = item.item_sales_tax_ref_list_id
                each_invoice.class_ref_list_id = item.class_ref_list_id

                if invoice is not None:
                    copy(each_invoice, invoice,
                         ignores=['id', 'is_active', 'created_date', 'updated_date', 'updated_by', 'created_by'])
                    for line in item.ext_details:
                        old_invoice_detail = db.session.query(invoice_detail_model).filter(
                            invoice_detail_model.txn_line_id == line['txn_line_id'],
                            invoice_detail_model.is_active == 't').first()
                        if old_invoice_detail is not None:
                            invoice_detail = invoice_detail_model()
                            invoice_detail.txn_line_id = line['txn_line_id']
                            invoice_detail.txn_invoice_id = line['txn_invoice_id']
                            invoice_detail.item_list_id = line['item_list_id']
                            invoice_detail.item_name = line['item_name']
                            invoice_detail.description = line['description']
                            invoice_detail.qty = line['quantity']
                            invoice_detail.price = line['price']
                            invoice_detail.class_list_id = line['class_list_id']
                            invoice_detail.sales_tax_code_list_id = line['sales_tax_code_list_id']
                            copy(invoice_detail, old_invoice_detail,
                                 ignores=['id', 'is_active', 'created_date', 'updated_date', 'updated_by',
                                          'created_by'])
                            db.session.commit()
                        else:
                            invoice_detail = invoice_detail_model()
                            invoice_detail.txn_line_id = line['txn_line_id']
                            invoice_detail.txn_invoice_id = line['txn_invoice_id']
                            invoice_detail.item_list_id = line['item_list_id']
                            invoice_detail.item_name = line['item_name']
                            invoice_detail.description = line['description']
                            invoice_detail.qty = line['quantity']
                            invoice_detail.price = line['price']
                            invoice_detail.class_list_id = line['class_list_id']
                            invoice_detail.sales_tax_code_list_id = line['sales_tax_code_list_id']
                            db.session.add(invoice_detail)
                            db.session.commit()

                else:
                    for line in item.ext_details:
                        invoice_detail = invoice_detail_model()
                        invoice_detail.txn_line_id = line['txn_line_id']
                        invoice_detail.txn_invoice_id = line['txn_invoice_id']
                        invoice_detail.item_list_id = line['item_list_id']
                        invoice_detail.item_name = line['item_name']
                        invoice_detail.description = line['description']
                        invoice_detail.qty = line['quantity']
                        invoice_detail.price = line['price']
                        invoice_detail.class_list_id = line['class_list_id']
                        invoice_detail.sales_tax_code_list_id = line['sales_tax_code_list_id']
                        db.session.add(invoice_detail)
                        db.session.commit()
                    db.session.add(each_invoice)
                db.session.commit()

            queue.data = str(data)
            queue.status = 1
            db.session.add(queue)
            db.session.commit()
            for biller_code in b24_biller_code_list:
                biller = db.session.query(company_b24_model).filter(company_b24_model.code == biller_code,
                                                                    company_b24_model.is_active == 't').first()
                if biller is not None:
                    token = biller.token
                    headers = {'content-type': "application/json", "token": token}
                    invoice_list_payload = []
                    ext__details = []
                    for invoice in payload:
                        for ext__detail in invoice.ext_details:
                            ext__details.append(
                                {
                                    "item_name": ext__detail['item_name'],
                                    "quantity": ext__detail['quantity'],
                                    "price": ext__detail['price'],
                                    "amount": ext__detail['amount']
                                }
                            )

                        invoice_list_payload.append(
                            {
                                "sync_code": invoice.txn_id,
                                "bill_date": invoice.txn_date,
                                "due_date": invoice.due_date,
                                "total_amount": invoice.total_amount,
                                "currency_id": invoice.currency_name,
                                "status": "approve",
                                "customer_sync_code": invoice.customer_list_id,
                                "customer_name": invoice.customer_name,
                                "bill_type": 2,
                                "ext__details": ext__details
                            }
                        )
                    supplier_api_url = settings_logic.get('supplier_api_url')
                    response = requests.post(url=f'{supplier_api_url}/bill/push', headers=headers,
                                             data=json.dumps({
                                                 "data": invoice_list_payload
                                             }))
                    if response.status_code == 200:
                        queue_detail = queue_detail_model()
                        queue_detail.queue_id = queue.id
                        queue_detail.b24_queue_id = json.loads(response.text)['id']
                        queue_detail.b24_biller_code = biller_code
                        queue_detail.data = ""
                        queue_detail.status = 1
                        db.session.add(queue_detail)
                        db.session.commit()

                    else:
                        raise HTTPException(status_code=response.status_code, detail='Push failed')
            return invoices_push_response(
                message="success",
                code="000",
                data={
                    "queue_id": queue.id,
                    "total_records": len(payload)
                }
            )
        else:
            raise HTTPException(status_code=401, detail={
                "message": "Unauthorized",
                "code": "401",
                "data": {}
            })

def copy(from_obj, to_obj, ignores=[]):
    """copy all properties from one oject to another object in the same sqlalchemy class.
    :param from_obj: source object that will copy attribue to destination object.
    :param to_obj: destination object tha will copy from source object.
    :param ignores: list of columns that will not override value from source object to destination object.
    """
    for key in [k for k in from_obj.__table__.columns.keys() if k not in ignores]:
        setattr(to_obj, key, getattr(from_obj, key))

        # fix .ext for ExtMixin
    # because .ext is just declare in ExtMixin not in .columns schema
    # we need to for copy it if source object contain that
    if hasattr(from_obj, 'ext'):
        to_obj.ext = from_obj.ext

    return to_obj


default = invoices_logics()

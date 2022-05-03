from sqlalchemy import Column, String, INT, ForeignKey, Boolean, DateTime, Float
from h602_central.models.base_model import base


class bank_model(base):
    __tablename__ = 'bank'
    id = Column('id', String(30), primary_key=True, unique=True)
    code = Column('code', String(100))
    name = Column('name', String(100))
    logo = Column('logo', String)


class company_model(base):
    __tablename__ = 'company'
    company_name_kh = Column('company_name_kh', String(100))
    company_name = Column('company_name', String(100))
    phone = Column('phone', String(100))
    email = Column('email', String(100))
    tin_number = Column('tin_number', String(100))
    address_kh = Column('address_kh', String(500))
    address = Column('address', String(500))


class company_authorize_model(base):
    __tablename__ = 'company_authorize'
    company_id = Column('company_id', INT, ForeignKey('company.id'))
    qe_token = Column('qe_token', String(500))


class company_b24_model(base):
    __tablename__ = 'company_b24'
    code = Column('code', String(50))
    token = Column('token', String(200))
    ar_account = Column('ar_account', String(300))
    currency = Column('currency', String(100))
    company_id = Column('company_id', INT, ForeignKey('company.id'))


class company_b24_bank_status_model(base):
    __tablename__ = 'company_b24_bank_status'

    company_b24_id = Column('company_b24_id', INT, ForeignKey('company_b24.id'))
    bank_id = Column('bank_id', String(30), ForeignKey(bank_model.id))
    status = Column('status', INT)


class register_model(base):
    __tablename__ = 'register'

    company_name_kh = Column('company_name_kh', String(100))
    company_name = Column('company_name', String(100))
    phone = Column('phone', String(100))
    email = Column('email', String(100))
    tin_number = Column('tin_number', String(100))
    address_kh = Column('address_kh', String(500))
    address = Column('address', String(500))
    file_document = Column('file_document', String)
    banks = Column('banks', String)
    status = Column('status', INT)
    qe_token = Column('qe_token', String(500))


class invoice_model(base):
    __tablename__ = 'invoice'
    b24_biller_code = Column('b24_biller_code', String(100))
    company_id = Column('company_id', String(100))
    txn_id = Column('txn_id', String(200))
    ref_number = Column('ref_number', String(200))
    txn_date = Column('txn_date', DateTime)
    due_date = Column('due_date', DateTime)
    customer_list_id = Column('customer_list_id', String(100))
    customer_name = Column('customer_name', String(200))
    exchange_rate = Column('exchange_rate', Float)
    currency_list_id = Column('currency_list_id', String(200))
    currency_name = Column('currency_name', String(100))
    bill_type = Column('bill_type', INT)
    status = Column('status', String)
    total_amount = Column('total_amount', Float)
    bill_address = Column('bill_address', String(500))
    ship_address = Column('ship_address', String(500))
    memo = Column('memo', String)
    is_pending = Column('is_pending', Boolean)
    po_number = Column('po_number', String)
    fob = Column('fob', String)
    ship_date = Column('ship_date', DateTime)
    sales_rep_list_id = Column('sales_rep_list_id', String(200))
    ship_method_list_id = Column('ship_method_list_id', String(200))
    ar_account_ref_list_id = Column('ar_account_ref_list_id', String(100))
    template_ref_list_id = Column('template_ref_list_id', String(100))
    terms_ref_list_id = Column('terms_ref_list_id', String(100))
    item_sales_tax_ref_list_id = Column('item_sales_tax_ref_list_id', String(100))
    class_ref_list_id = Column('class_ref_list_id', String(100))


class invoice_detail_model(base):
    __tablename__ = 'invoice_detail'
    txn_line_id = Column('txn_line_id', String(200))
    txn_invoice_id = Column('txn_invoice_id', String(200))
    item_list_id = Column('item_list_id', String(200))
    item_name = Column('item_name', String(200))
    description = Column('description', String)
    qty = Column('qty', Float)
    price = Column('price', Float)
    class_list_id = Column('class_list_id', String(200))
    sales_tax_code_list_id = Column('sales_tax_code_list_id', String(200))


class receive_payment_model(base):
    __tablename__ = 'receive_payment'
    b24_biller_code = Column(String(200))
    bank = Column('bank', String(100))
    bank_ref = Column('bank_ref', String(300))
    checkout_ref = Column('checkout_ref', String(300))
    currency = Column('currency', String(100))
    customer_code = Column('customer_code', String(200))
    customer_fee = Column('customer_fee', Float)
    customer_name = Column('customer_name', String(200))
    customer_phone = Column('customer_phone', String(200))
    customer_sync_code = Column('customer_sync_code', String(100))
    description = Column('description', String(500))
    paid_by = Column('paid_by', String(100))
    paid_date = Column('paid_date', DateTime)
    supplier_fee = Column('supplier_fee', Float)
    tnx_id = Column('tnx_id', String(100))
    total_amount = Column('total_amount', Float)
    tran_amount = Column('tran_amount', Float)
    bills = Column('bills', String)

# class receive_payment_detail_model(base):
#     __tablename__ = 'receive_payment_detail'
#     sync_code = Column('sync_code', String(200))
#     code = Column('code', String(200))
#     org_code = Column('org_code', String(200))
#     customer_sync_code = Column('customer_sync_code', String(200))
#     total_amount = Column('total_amount', Float)
#     pay_amount = Column('pay_amount', String(200))
#     due_amount = Column('due_amount', String(200))
#     txn_receive_payment_id = Column('txn_receive_payment_id', INT, ForeignKey('receive_payment.id'))
#     txn_date = Column('txn_date', DateTime)
#     due_date = Column('due_date', DateTime)


class settings_model(base):
    __tablename__ = 'settings'
    id = Column(String, primary_key=True)
    name = Column(String)
    datatype = Column(String)
    value = Column(String)
    is_active = Column(String)


class queue_model(base):
    __tablename__ = 'queue'
    company_id = Column(INT)
    date = Column(DateTime)
    type = Column(INT)
    total_record = Column(INT)
    data = Column(String)
    status = Column(INT)


class queue_detail_model(base):
    __tablename__ = 'queue_detail'
    queue_id = Column(INT)
    b24_queue_id = Column(String(100))
    b24_biller_code = Column(String(500))
    data = Column(String)
    status = Column(INT)










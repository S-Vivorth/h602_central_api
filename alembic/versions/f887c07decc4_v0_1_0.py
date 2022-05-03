"""v0_1_0

Revision ID: f887c07decc4
Revises: 
Create Date: 2022-04-21 22:42:38.363031

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, INT, Column, Float, ForeignKey


# revision identifiers, used by Alembic.
revision = 'f887c07decc4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('register',
                    sa.Column('id', INT, primary_key=True, unique=True, autoincrement=True),
                    sa.Column('company_name_kh', sa.String(100)),
                    sa.Column('company_name', sa.String(100)),
                    sa.Column('phone', sa.String(100)),
                    sa.Column('email', sa.String(100)),
                    sa.Column('tin_number', sa.String(100)),
                    sa.Column('address_kh', sa.String(500)),
                    sa.Column('address', sa.String(500)),
                    sa.Column('file_document', sa.String),
                    sa.Column('banks', sa.String),
                    sa.Column('status', sa.INT),
                    sa.Column('qe_token', String(500)),
                    Column('is_active', sa.Boolean))
    op.create_table('company',
                    sa.Column('id', INT, primary_key=True, unique=True),
                    sa.Column('company_name_kh', sa.String(100)),
                    sa.Column('company_name', sa.String(100)),
                    sa.Column('phone', sa.String(100)),
                    sa.Column('email', sa.String(100)),
                    sa.Column('tin_number', sa.String(100)),
                    sa.Column('address_kh', sa.String(500)),
                    sa.Column('address', sa.String(500)),
                    Column('is_active', sa.Boolean))

    op.create_table('company_authorize',
                    sa.Column('id', INT, primary_key=True, unique=True),
                    sa.Column('company_id', INT, ForeignKey('company.id')),
                    sa.Column('qe_token', String(500)),
                    Column('is_active', sa.Boolean))

    op.create_table('company_b24',
                    Column('id', INT, primary_key=True, unique=True),
                    Column('code', String(50)),
                    Column('token', String(200)),
                    Column('company_id', INT, ForeignKey('company.id')),
                    Column('is_active', sa.Boolean))

    op.create_table('bank',
                    Column('id', String(30), primary_key=True, unique=True),
                    Column('code', String(100)),
                    Column('name', String(100)),
                    Column('logo', String),
                    Column('is_active', sa.Boolean))

    op.create_table('company_b24_bank_status',
                    Column('id', INT, primary_key=True, unique=True),
                    Column('company_b24_id', INT, ForeignKey('company_b24.id')),
                    Column('bank_id', String(30), ForeignKey('bank.id')),
                    Column('status', INT),
                    Column('is_active', sa.Boolean))
    op.create_table('invoice',
                    Column('id', INT, primary_key=True, unique=True),
                    Column('b24_biller_code', String(100)),
                    Column('company_id', String(100)),
                    Column('txn_id', String(200)),
                    Column('ref_number', String(200)),
                    Column('txn_date', sa.DateTime),
                    Column('due_date', sa.DateTime),
                    Column('customer_list_id', String(100)),
                    Column('customer_name', String(200)),
                    Column('exchange_rate', sa.Float),
                    Column('currency_list_id', String(200)),
                    Column('currency_name', String(100)),
                    Column('bill_type', INT),
                    Column('status', String),
                    Column('total_amount', sa.Float),
                    Column('bill_address', String(500)),
                    Column('ship_address', String(500)),
                    Column('memo', String),
                    Column('is_pending', sa.Boolean),
                    Column('po_number', String),
                    Column('fob', String),
                    Column('ship_date', sa.DateTime),
                    Column('sales_rep_list_id', String(200)),
                    Column('ship_method_list_id', String(200)),
                    Column('ar_account_ref_list_id', String(100)),
                    Column('template_ref_list_id', String(100)),
                    Column('terms_ref_list_id', String(100)),
                    Column('item_sales_tax_ref_list_id', String(100)),
                    Column('class_ref_list_id', String(100)),
                    Column('is_active', sa.Boolean)
                    )

    op.create_table('invoice_detail',
                    Column('id', INT, primary_key=True, unique=True),
                    Column('txn_line_id', String(200)),
                    Column('txn_invoice_id', String(200)),
                    Column('item_list_id', String(200)),
                    Column('item_name', String(200)),
                    Column('description', String),
                    Column('qty', sa.Float),  # suppose to be int?
                    Column('price', sa.Float),
                    Column('class_list_id', String(200)),
                    Column('sales_tax_code_list_id', String(200)),
                    Column('is_active', sa.Boolean)
                    )

    op.create_table('receive_payment',
                    Column('id', INT, primary_key=True, unique=True),
                    Column('code', String(100)),
                    Column('title', String(200)),
                    Column('tran_date', sa.DateTime),
                    Column('description', String),
                    Column('payment_type', String(200)),
                    Column('payment_method', String(500)),
                    Column('tran_amount', sa.Float),
                    Column('fee_amount', sa.Float),
                    Column('total_amount', sa.Float),
                    Column('supplier_fee', sa.Float),
                    Column('currency_id', String(200)),
                    Column('customer_sync_code', String(100)),
                    Column('customer_org_code', String(100)),
                    Column('customer_name', String(200)),
                    Column('sync_code', String(100)),
                    Column('source', String),
                    Column('payment_ref', String(200)),
                    Column('bank_id', String(200)),
                    Column('bank_name', String(200)),
                    Column('paid_to', String(200)),
                    Column('pay_by', String(200)),
                    Column('is_active', sa.Boolean)
                    )
    op.create_table('receive_payment_detail',
                    Column('id', INT, primary_key=True, unique=True),
                    Column('sync_code', String(200)),
                    Column('code', String(200)),
                    Column('org_code', String(200)),
                    Column('customer_sync_code', String(200)),
                    Column('total_amount', sa.Float),
                    Column('pay_amount', String(200)),
                    Column('due_amount', String(200)),
                    Column('txn_receive_payment_id', INT, ForeignKey('receive_payment.id')),
                    Column('txn_date', sa.DateTime),
                    Column('due_date', sa.DateTime),
                    Column('is_active', sa.Boolean)
                    )
    pass


def downgrade():
    pass

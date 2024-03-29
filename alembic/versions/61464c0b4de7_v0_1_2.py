"""v0_1_2

Revision ID: 61464c0b4de7
Revises: 18a5d8b6b032
Create Date: 2022-04-25 10:54:58.413553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61464c0b4de7'
down_revision = '18a5d8b6b032'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bank', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('bank', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('bank', sa.Column('updated_by', sa.String(length=200), nullable=True))
    op.add_column('bank', sa.Column('created_by', sa.String(length=200), nullable=True))
    op.add_column('company', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('company', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('company', sa.Column('updated_by', sa.String(length=200), nullable=True))
    op.add_column('company', sa.Column('created_by', sa.String(length=200), nullable=True))
    op.add_column('company_authorize', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('company_authorize', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('company_authorize', sa.Column('updated_by', sa.String(length=200), nullable=True))
    op.add_column('company_authorize', sa.Column('created_by', sa.String(length=200), nullable=True))
    op.add_column('company_b24', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('company_b24', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('company_b24', sa.Column('updated_by', sa.String(length=200), nullable=True))
    op.add_column('company_b24', sa.Column('created_by', sa.String(length=200), nullable=True))
    op.add_column('company_b24_bank_status', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('company_b24_bank_status', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('company_b24_bank_status', sa.Column('updated_by', sa.String(length=200), nullable=True))
    op.add_column('company_b24_bank_status', sa.Column('created_by', sa.String(length=200), nullable=True))
    op.add_column('invoice', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('invoice', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('invoice', sa.Column('updated_by', sa.String(length=200), nullable=True))
    op.add_column('invoice', sa.Column('created_by', sa.String(length=200), nullable=True))
    op.add_column('invoice_detail', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('invoice_detail', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('invoice_detail', sa.Column('updated_by', sa.String(length=200), nullable=True))
    op.add_column('invoice_detail', sa.Column('created_by', sa.String(length=200), nullable=True))
    op.add_column('receive_payment', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('receive_payment', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('receive_payment', sa.Column('updated_by', sa.String(length=200), nullable=True))
    op.add_column('receive_payment', sa.Column('created_by', sa.String(length=200), nullable=True))
    op.add_column('receive_payment_detail', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('receive_payment_detail', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('receive_payment_detail', sa.Column('updated_by', sa.String(length=200), nullable=True))
    op.add_column('receive_payment_detail', sa.Column('created_by', sa.String(length=200), nullable=True))
    op.add_column('register', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('register', sa.Column('updated_date', sa.DateTime(), nullable=True))
    op.add_column('register', sa.Column('updated_by', sa.String(length=200), nullable=True))
    op.add_column('register', sa.Column('created_by', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('register', 'created_by')
    op.drop_column('register', 'updated_by')
    op.drop_column('register', 'updated_date')
    op.drop_column('register', 'created_date')
    op.drop_column('receive_payment_detail', 'created_by')
    op.drop_column('receive_payment_detail', 'updated_by')
    op.drop_column('receive_payment_detail', 'updated_date')
    op.drop_column('receive_payment_detail', 'created_date')
    op.drop_column('receive_payment', 'created_by')
    op.drop_column('receive_payment', 'updated_by')
    op.drop_column('receive_payment', 'updated_date')
    op.drop_column('receive_payment', 'created_date')
    op.drop_column('invoice_detail', 'created_by')
    op.drop_column('invoice_detail', 'updated_by')
    op.drop_column('invoice_detail', 'updated_date')
    op.drop_column('invoice_detail', 'created_date')
    op.drop_column('invoice', 'created_by')
    op.drop_column('invoice', 'updated_by')
    op.drop_column('invoice', 'updated_date')
    op.drop_column('invoice', 'created_date')
    op.drop_column('company_b24_bank_status', 'created_by')
    op.drop_column('company_b24_bank_status', 'updated_by')
    op.drop_column('company_b24_bank_status', 'updated_date')
    op.drop_column('company_b24_bank_status', 'created_date')
    op.drop_column('company_b24', 'created_by')
    op.drop_column('company_b24', 'updated_by')
    op.drop_column('company_b24', 'updated_date')
    op.drop_column('company_b24', 'created_date')
    op.drop_column('company_authorize', 'created_by')
    op.drop_column('company_authorize', 'updated_by')
    op.drop_column('company_authorize', 'updated_date')
    op.drop_column('company_authorize', 'created_date')
    op.drop_column('company', 'created_by')
    op.drop_column('company', 'updated_by')
    op.drop_column('company', 'updated_date')
    op.drop_column('company', 'created_date')
    op.drop_column('bank', 'created_by')
    op.drop_column('bank', 'updated_by')
    op.drop_column('bank', 'updated_date')
    op.drop_column('bank', 'created_date')
    op.create_table('settings',
    sa.Column('id', sa.VARCHAR(length=8), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('datatype', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('value', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='settings_pkey')
    )
    # ### end Alembic commands ###

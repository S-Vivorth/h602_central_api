"""v0_1_1

Revision ID: 18a5d8b6b032
Revises: f887c07decc4
Create Date: 2022-04-21 22:44:43.014572

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, INT, Column, Float, ForeignKey


# revision identifiers, used by Alembic.
revision = '18a5d8b6b032'
down_revision = 'f887c07decc4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('settings',
                    Column('id', sa.String(8), primary_key=True, unique=True),
                    Column('name', sa.String(500)),
                    Column('datatype', sa.String(20)),
                    Column('value', sa.String),
                    Column('is_active', sa.Boolean))
    pass


def downgrade():
    pass

"""empty message

Revision ID: e82e51408a37
Revises: a93c29c70066
Create Date: 2023-12-30 04:44:45.990113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e82e51408a37'
down_revision = 'a93c29c70066'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('record_date', sa.String(), nullable=True),
    sa.Column('ap_number', sa.String(), nullable=True),
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.Column('invoice_number', sa.String(), nullable=True),
    sa.Column('receiving_number', sa.String(), nullable=True),
    sa.Column('po_number', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payable_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payable_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.Column('measure_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('sales_tax_id', sa.Integer(), nullable=False),
    sa.Column('w_tax_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['measure_id'], ['measure.id'], ),
    sa.ForeignKeyConstraint(['payable_id'], ['payable.id'], ),
    sa.ForeignKeyConstraint(['sales_tax_id'], ['sales_tax.id'], ),
    sa.ForeignKeyConstraint(['w_tax_id'], ['w_tax.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payable_detail')
    op.drop_table('payable')
    # ### end Alembic commands ###

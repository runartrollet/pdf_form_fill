"""empty message

Revision ID: ff77f008aee2
Revises: c33d3fc0dca7
Create Date: 2017-07-29 13:17:38.973175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff77f008aee2'
down_revision = 'c33d3fc0dca7'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.drop_table('room')
    op.add_column('filled_form', sa.Column('customer_id', sa.Integer(), nullable=True))
    op.drop_constraint('filled_form_company_id_fkey', 'filled_form', type_='foreignkey')
    op.drop_constraint('filled_form_address_id_fkey', 'filled_form', type_='foreignkey')
    op.create_foreign_key(None, 'filled_form', 'customer', ['customer_id'], ['id'])
    op.drop_column('filled_form', 'address_id')
    op.drop_column('filled_form', 'company_id')
    op.drop_column('filled_form', 'customer_name')
    op.add_column('filled_form_modified', sa.Column('room_id', sa.Integer(), nullable=True))
    op.drop_constraint('filled_form_modified_filled_form_id_fkey', 'filled_form_modified', type_='foreignkey')
    op.create_foreign_key(None, 'filled_form_modified', 'filled_form', ['room_id'], ['id'])
    op.drop_column('filled_form_modified', 'filled_form_id')
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('filled_form_modified', sa.Column('filled_form_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'filled_form_modified', type_='foreignkey')
    op.create_foreign_key('filled_form_modified_filled_form_id_fkey', 'filled_form_modified', 'filled_form', ['filled_form_id'], ['id'])
    op.drop_column('filled_form_modified', 'room_id')
    op.add_column('filled_form', sa.Column('customer_name', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
    op.add_column('filled_form', sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('filled_form', sa.Column('address_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'filled_form', type_='foreignkey')
    op.create_foreign_key('filled_form_address_id_fkey', 'filled_form', 'address', ['address_id'], ['id'])
    op.create_foreign_key('filled_form_company_id_fkey', 'filled_form', 'company', ['company_id'], ['id'])
    op.drop_column('filled_form', 'customer_id')
    op.create_table('room',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], name='room_company_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='room_pkey')
    )
    op.drop_table('customer')
    # ### end Alembic commands ###


def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


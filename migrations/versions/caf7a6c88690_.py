"""empty message

Revision ID: caf7a6c88690
Revises: db2af8b2f3fe
Create Date: 2017-10-08 17:23:03.184458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'caf7a6c88690'
down_revision = 'db2af8b2f3fe'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'address', ['id'])
    op.add_column('company', sa.Column('contact_mobile', sa.String(length=20), nullable=True))
    op.add_column('company', sa.Column('installer_name', sa.String(length=200), nullable=False,
    server_default=''))
    op.create_unique_constraint(None, 'company', ['id'])
    op.create_unique_constraint(None, 'contact', ['id'])
    op.add_column('customer', sa.Column('address2_id', sa.Integer(), nullable=True))
    op.add_column('customer', sa.Column('construction_change', sa.Boolean(), nullable=True))
    op.add_column('customer', sa.Column('construction_nek400', sa.Boolean(), nullable=True))
    op.add_column('customer', sa.Column('construction_new', sa.Boolean(), nullable=True))
    op.add_column('customer', sa.Column('construction_voltage', sa.Integer(), nullable=True))
    op.add_column('customer', sa.Column('name2', sa.String(length=100), nullable=True))
    op.add_column('customer', sa.Column('orgnumber', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'customer', ['id'])
    op.create_foreign_key(None, 'customer', 'address', ['address2_id'], ['id'])
    op.create_unique_constraint(None, 'inside_specs', ['id'])
    op.create_unique_constraint(None, 'invite', ['id'])
    op.create_unique_constraint(None, 'outside_specs', ['id'])
    op.create_unique_constraint(None, 'room', ['id'])
    op.create_unique_constraint(None, 'room_item', ['id'])
    op.create_unique_constraint(None, 'room_item_modifications', ['id'])
    op.create_unique_constraint(None, 'room_type_info', ['id'])
    op.create_unique_constraint(None, 'user_contact', ['id'])
    op.create_unique_constraint(None, 'vk_users', ['id'])
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'vk_users', type_='unique')
    # op.drop_constraint(None, 'user_contact', type_='unique')
    # op.drop_constraint(None, 'room_type_info', type_='unique')
    # op.drop_constraint(None, 'room_item_modifications', type_='unique')
    # op.drop_constraint(None, 'room_item', type_='unique')
    # op.drop_constraint(None, 'room', type_='unique')
    # op.drop_constraint(None, 'outside_specs', type_='unique')
    # op.drop_constraint(None, 'invite', type_='unique')
    # op.drop_constraint(None, 'inside_specs', type_='unique')
    # op.drop_constraint(None, 'customer', type_='foreignkey')
    # op.drop_constraint(None, 'customer', type_='unique')
    op.drop_column('customer', 'orgnumber')
    op.drop_column('customer', 'name2')
    op.drop_column('customer', 'construction_voltage')
    op.drop_column('customer', 'construction_new')
    op.drop_column('customer', 'construction_nek400')
    op.drop_column('customer', 'construction_change')
    op.drop_column('customer', 'address2_id')
    # op.drop_constraint(None, 'contact', type_='unique')
    # op.drop_constraint(None, 'company', type_='unique')
    op.drop_column('company', 'installer_name')
    op.drop_column('company', 'contact_mobile')
    # op.drop_constraint(None, 'address', type_='unique')
    # ### end Alembic commands ###


def upgrade_products():
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_unique_constraint(None, 'manufacturor', ['id'])
    # op.create_unique_constraint(None, 'product', ['id'])
    # op.create_unique_constraint(None, 'product_type', ['id'])
    # ### end Alembic commands ###


def downgrade_products():
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'product_type', type_='unique')
    # op.drop_constraint(None, 'product', type_='unique')
    # op.drop_constraint(None, 'manufacturor', type_='unique')
    # ### end Alembic commands ###

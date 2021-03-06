"""empty message

Revision ID: 3be8c0a07968
Revises: caf7a6c88690
Create Date: 2017-10-10 13:45:59.566098

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '3be8c0a07968'
down_revision = 'caf7a6c88690'
branch_labels = None
depends_on = None

customerHelper = sa.Table(
    'customer',
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('address_id', sa.Integer),
    sa.Column('owner_id', sa.Integer),)


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    op.create_table(
        'customer_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('address_id', sa.Integer(), nullable=False),
        sa.Column('orgnumber', sa.Integer(), nullable=True),
        sa.Column('contact_name', sa.String(length=200), nullable=True),
        sa.Column('contact_phone', sa.String(length=20), nullable=True),
        sa.Column('contact_mobile', sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(
            ['address_id'],
            ['address.id'],),
        sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('id'))
    op.add_column('customer',
                  sa.Column('construction_id', sa.Integer(), nullable=True))
    op.add_column('customer',
                  sa.Column('owner_id', sa.Integer()))
    op.create_foreign_key(None, 'customer', 'customer_data',
                          ['construction_id'], ['id'])
    op.create_foreign_key(None, 'customer', 'customer_data', ['owner_id'],
                          ['id'])
    i = 0
    for customer in connection.execute(customerHelper.select()):
        i += 1
        address_id = customer.address_id
        op.execute(
            'INSERT into customer_data (id, address_id) values ( {},{} )'\
            .format(i, address_id))
        connection.execute(customerHelper.update().where(
            customerHelper.c.id == customer.id).values(owner_id=i,))
    op.drop_constraint(
        'customer_address_id_fkey', 'customer', type_='foreignkey')
    op.drop_constraint(
        'customer_address2_id_fkey', 'customer', type_='foreignkey')
    op.drop_column('customer', 'address_id')
    op.drop_column('customer', 'name2')
    op.drop_column('customer', 'orgnumber')
    op.drop_column('customer', 'address2_id')
    op.alter_column('customer', 'owner_id', nullable=False)
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer',
                  sa.Column(
                      'address2_id',
                      sa.INTEGER(),
                      autoincrement=False,
                      nullable=True))
    op.add_column('customer',
                  sa.Column(
                      'orgnumber',
                      sa.INTEGER(),
                      autoincrement=False,
                      nullable=True))
    op.add_column('customer',
                  sa.Column(
                      'name2',
                      sa.VARCHAR(length=100),
                      autoincrement=False,
                      nullable=True))
    op.add_column('customer',
                  sa.Column(
                      'address_id',
                      sa.INTEGER(),
                      autoincrement=False,
                      nullable=False))
    op.drop_constraint(None, 'customer', type_='foreignkey')
    op.drop_constraint(None, 'customer', type_='foreignkey')
    op.create_foreign_key('customer_address2_id_fkey', 'customer', 'address',
                          ['address2_id'], ['id'])
    op.create_foreign_key('customer_address_id_fkey', 'customer', 'address',
                          ['address_id'], ['id'])
    op.drop_column('customer', 'owner_id')
    op.drop_column('customer', 'construction_id')
    op.drop_table('customer_data')
    # ### end Alembic commands ###


def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'manufacturor', ['id'])
    op.create_unique_constraint(None, 'product', ['id'])
    op.create_unique_constraint(None, 'product_type', ['id'])
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_type', type_='unique')
    op.drop_constraint(None, 'product', type_='unique')
    op.drop_constraint(None, 'manufacturor', type_='unique')
    # ### end Alembic commands ###

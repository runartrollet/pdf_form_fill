"""empty message

Revision ID: 66167a61148c
Revises: 5feba6ec741c
Create Date: 2017-09-03 12:24:38.587084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66167a61148c'
down_revision = '5feba6ec741c'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('date', sa.DateTime(), nullable=True))
    op.add_column('customer', sa.Column('modified_on_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer', 'modified_on_date')
    op.drop_column('customer', 'date')
    # ### end Alembic commands ###


def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

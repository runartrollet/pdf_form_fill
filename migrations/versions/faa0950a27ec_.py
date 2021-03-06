"""empty message

Revision ID: faa0950a27ec
Revises: d4d76b9ef4cc
Create Date: 2017-08-19 15:43:05.625305

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'faa0950a27ec'
down_revision = 'd4d76b9ef4cc'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room_types_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('normalEffect', sa.SmallInteger(), nullable=False),
    sa.Column('maxEffect', sa.SmallInteger(), nullable=False),
    sa.Column('names', postgresql.ARRAY(sa.String(), dimensions=1), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room_types_info')
    # ### end Alembic commands ###


def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


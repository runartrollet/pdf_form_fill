"""empty message

Revision ID: 2368ae874fda
Revises: 4fb71d79ceed
Create Date: 2017-08-10 19:41:47.990708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2368ae874fda'
down_revision = '4fb71d79ceed'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room_item_modifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('archived', sa.Boolean(), nullable=True),
    sa.Column('room_item_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('json', sa.JSON(), nullable=False),
    sa.Column('pdf_json', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['room_item_id'], ['room_item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['vk_users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room_item_modifications')
    # ### end Alembic commands ###


def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


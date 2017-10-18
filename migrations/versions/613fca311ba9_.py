"""Add more columns for Oegloand

Revision ID: 613fca311ba9
Revises: 22813fdedef8
Create Date: 2017-09-29 13:31:44.775168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '613fca311ba9'
down_revision = '22813fdedef8'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inside_specs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('LamiFlex', sa.Boolean(), nullable=True),
    sa.Column('low_profile', sa.Boolean(), nullable=True),
    sa.Column('fireproof', sa.Boolean(), nullable=True),
    sa.Column('frost_protection_pipe', sa.Boolean(), nullable=True),
    sa.Column('concrete', sa.Boolean(), nullable=True),
    sa.Column('other', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('outside_specs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asphalt', sa.Boolean(), nullable=True),
    sa.Column('paving_stones', sa.Boolean(), nullable=True),
    sa.Column('vessel', sa.Boolean(), nullable=True),
    sa.Column('frost_protection', sa.Boolean(), nullable=True),
    sa.Column('frost_protection_pipe', sa.Boolean(), nullable=True),
    sa.Column('concrete', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.add_column('room', sa.Column('handed_to_owner', sa.Boolean(), nullable=True))
    op.add_column('room', sa.Column('inside_id', sa.Integer(), nullable=True))
    op.add_column('room', sa.Column('outside_id', sa.Integer(), nullable=True))
    op.add_column('room', sa.Column('owner_informed', sa.Boolean(), nullable=True))
    op.create_foreign_key(None, 'room', 'inside_specs', ['inside_id'], ['id'])
    op.create_foreign_key(None, 'room', 'outside_specs', ['outside_id'], ['id'])
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'room', type_='foreignkey')
    op.drop_constraint(None, 'room', type_='foreignkey')
    op.drop_column('room', 'owner_informed')
    op.drop_column('room', 'outside_id')
    op.drop_column('room', 'inside_id')
    op.drop_column('room', 'handed_to_owner')
    op.drop_table('outside_specs')
    op.drop_table('inside_specs')
    # ### end Alembic commands ###


def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
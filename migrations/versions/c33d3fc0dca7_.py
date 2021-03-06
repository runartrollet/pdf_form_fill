"""empty message

Revision ID: c33d3fc0dca7
Revises: a0792ed2ba6a
Create Date: 2017-07-18 19:24:33.834815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c33d3fc0dca7'
down_revision = 'a0792ed2ba6a'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_unique_constraint(None, 'address', ['id'])
    op.create_unique_constraint(None, 'company', ['id'])
    op.create_unique_constraint(None, 'company_contact', ['id'])
    op.create_unique_constraint(None, 'contact', ['id'])
    op.create_unique_constraint(None, 'filled_form', ['id'])
    op.create_unique_constraint(None, 'filled_form_modified', ['id'])
    op.create_unique_constraint(None, 'invite', ['id'])
    op.create_unique_constraint(None, 'user_contact', ['id'])
    op.create_unique_constraint(None, 'vk_users', ['id'])
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vk_users', type_='unique')
    op.drop_constraint(None, 'user_contact', type_='unique')
    op.drop_constraint(None, 'invite', type_='unique')
    op.drop_constraint(None, 'filled_form_modified', type_='unique')
    op.drop_constraint(None, 'filled_form', type_='unique')
    op.drop_constraint(None, 'contact', type_='unique')
    op.drop_constraint(None, 'company_contact', type_='unique')
    op.drop_constraint(None, 'company', type_='unique')
    op.drop_constraint(None, 'address', type_='unique')
    op.drop_table('room')
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


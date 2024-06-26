"""added user_id as foreign key oon task table

Revision ID: 82b8f19b4d96
Revises: 5955491f12e8
Create Date: 2024-03-29 17:25:21.627801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82b8f19b4d96'
down_revision = '5955491f12e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###

"""empty message

Revision ID: abe3f9280a1c
Revises: 62ef15b0c411
Create Date: 2024-11-28 11:43:38.491265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abe3f9280a1c'
down_revision = '62ef15b0c411'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###

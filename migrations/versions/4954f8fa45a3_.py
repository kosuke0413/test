"""empty message

Revision ID: 4954f8fa45a3
Revises: b0b512a83562
Create Date: 2024-11-21 14:03:08.753934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4954f8fa45a3'
down_revision = 'b0b512a83562'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('local_id', sa.String(length=3), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.Column('mailaddress', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
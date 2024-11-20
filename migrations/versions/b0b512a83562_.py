"""empty message

Revision ID: b0b512a83562
Revises: bb2a3bf54c3d
Create Date: 2024-11-20 10:31:42.987582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0b512a83562'
down_revision = 'bb2a3bf54c3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notice', schema=None) as batch_op:
        batch_op.add_column(sa.Column('notice_text', sa.Text(), nullable=False))
        batch_op.drop_column('content')

    with op.batch_alter_table('notice_reply', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reply_text', sa.Text(), nullable=False))
        batch_op.drop_column('content')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notice_reply', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False))
        batch_op.drop_column('reply_text')

    with op.batch_alter_table('notice', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False))
        batch_op.drop_column('notice_text')

    # ### end Alembic commands ###

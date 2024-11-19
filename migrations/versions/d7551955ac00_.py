"""empty message

Revision ID: d7551955ac00
Revises: 6ba552e8d569
Create Date: 2024-11-19 01:52:12.161095

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd7551955ac00'
down_revision = '6ba552e8d569'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notice',
    sa.Column('notice_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.Column('tag', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('notice_id')
    )
    op.create_table('post',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('post_title', sa.String(length=30), nullable=True),
    sa.Column('post_text', sa.String(length=200), nullable=True),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.Column('tag', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.drop_table('Notice')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Notice',
    sa.Column('notice_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('image', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.Column('tag', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('notice_id', name='Notice_pkey')
    )
    op.drop_table('post')
    op.drop_table('notice')
    # ### end Alembic commands ###
"""empty message

Revision ID: 4c8869c4f2bb
Revises: 974785f25f9d
Create Date: 2024-11-19 11:42:04.009473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c8869c4f2bb'
down_revision = '974785f25f9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('local',
    sa.Column('local_id', sa.Integer(), nullable=True),
    sa.Column('local_name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('local_id')
    )
    op.create_table('notice_reply',
    sa.Column('notice_id', sa.Integer(), nullable=False),
    sa.Column('reply_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('reply_id')
    )
    op.create_table('post_reply',
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('reply_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('reply_id')
    )
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('tag_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('tag_id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.VARCHAR(),
               type_=sa.LargeBinary(),
               existing_nullable=True,
                postgresql_using="image::bytea")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    op.drop_table('tags')
    op.drop_table('post_reply')
    op.drop_table('notice_reply')
    op.drop_table('local')
    # ### end Alembic commands ###

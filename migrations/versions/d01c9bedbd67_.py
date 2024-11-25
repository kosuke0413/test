"""empty message

Revision ID: d01c9bedbd67
Revises: 
Create Date: 2024-11-22 12:10:17.349293


"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd01c9bedbd67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notice', schema=None) as batch_op:
        batch_op.alter_column('tag',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Integer(),
               postgresql_using="tag::integer")

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('tag',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Integer(),
               postgresql_using="tag::integer")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('tag',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)

    with op.batch_alter_table('notice', schema=None) as batch_op:
        batch_op.alter_column('tag',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###

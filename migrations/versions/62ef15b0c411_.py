"""empty message

Revision ID: 62ef15b0c411
Revises: e98c6f8009dd
Create Date: 2024-11-26 14:49:17.030176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62ef15b0c411'
down_revision = 'e98c6f8009dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('local', schema=None) as batch_op:
        batch_op.alter_column('local_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=3),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('local', schema=None) as batch_op:
        batch_op.alter_column('local_id',
               existing_type=sa.String(length=3),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###

"""third

Revision ID: 8594a58a62eb
Revises: b392c36f5f4c
Create Date: 2024-10-31 03:13:53.595019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8594a58a62eb'
down_revision = 'b392c36f5f4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=128), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
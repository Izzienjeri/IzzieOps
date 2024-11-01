"""done

Revision ID: f89a759a966b
Revises: b6159fe3dfb3
Create Date: 2024-11-01 06:42:27.151741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f89a759a966b'
down_revision = 'b6159fe3dfb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=256), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
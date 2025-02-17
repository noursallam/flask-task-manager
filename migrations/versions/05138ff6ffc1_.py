"""empty message

Revision ID: 05138ff6ffc1
Revises: a57cad2d7141
Create Date: 2025-02-17 12:54:53.619238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05138ff6ffc1'
down_revision = 'a57cad2d7141'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Priority', sa.String(length=50), nullable=True))
        batch_op.drop_column('priority')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('priority', sa.VARCHAR(length=50), nullable=True))
        batch_op.drop_column('Priority')

    # ### end Alembic commands ###

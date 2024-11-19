"""empty message

Revision ID: e5c0b8f1b7b6
Revises: 70ae8ad9160a
Create Date: 2024-11-19 16:20:54.103716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5c0b8f1b7b6'
down_revision = '70ae8ad9160a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('birth_day',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('birth_month',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('birth_year',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('birth_year',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('birth_month',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('birth_day',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###

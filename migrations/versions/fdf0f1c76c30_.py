"""empty message

Revision ID: fdf0f1c76c30
Revises: a1906b37d3e1
Create Date: 2022-09-26 19:18:28.790809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdf0f1c76c30'
down_revision = 'a1906b37d3e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource', sa.Column('is_out_of_date', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resource', 'is_out_of_date')
    # ### end Alembic commands ###

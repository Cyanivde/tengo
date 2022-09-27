"""empty message

Revision ID: 8405d132220c
Revises: 90dcf2a08c47
Create Date: 2022-09-27 09:13:45.559129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8405d132220c'
down_revision = '90dcf2a08c47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource_to_user', sa.Column('like', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resource_to_user', 'like')
    # ### end Alembic commands ###

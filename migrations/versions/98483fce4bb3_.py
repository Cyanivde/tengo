"""empty message

Revision ID: 98483fce4bb3
Revises: 05ca05ea1f92
Create Date: 2022-08-17 17:30:21.058314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98483fce4bb3'
down_revision = '05ca05ea1f92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource', sa.Column('recording', sa.String(length=500), nullable=True))
    op.add_column('resource', sa.Column('comments', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resource', 'comments')
    op.drop_column('resource', 'recording')
    # ### end Alembic commands ###

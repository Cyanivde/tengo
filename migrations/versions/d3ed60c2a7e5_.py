"""empty message

Revision ID: d3ed60c2a7e5
Revises: 2d9d9d53ba20
Create Date: 2022-08-28 22:03:03.240612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3ed60c2a7e5'
down_revision = '2d9d9d53ba20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('course', 'id',
                    nullable=False, new_column_name='course_id')
    op.alter_column('resource', 'id',
                    nullable=False, new_column_name='resource_id')
    op.alter_column('subject', 'id',
                    nullable=False, new_column_name='subject_id')
    op.alter_column('user', 'id',
                    nullable=False, new_column_name='user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('course', 'course_id',
                    nullable=False, new_column_name='id')
    op.alter_column('resource', 'resource_id',
                    nullable=False, new_column_name='id')
    op.alter_column('subject', 'subject_id',
                    nullable=False, new_column_name='id')
    op.alter_column('user', 'user_id',
                    nullable=False, new_column_name='id')
    # ### end Alembic commands ###
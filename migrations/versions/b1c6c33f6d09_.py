"""empty message

Revision ID: b1c6c33f6d09
Revises: a3f5843ae82b
Create Date: 2023-02-18 19:19:18.884356

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b1c6c33f6d09'
down_revision = 'a3f5843ae82b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('course')
    op.add_column('resource', sa.Column('folder', sa.String(length=50), nullable=True))
    op.add_column('resource', sa.Column('creator', sa.String(length=50), nullable=True))
    op.drop_column('resource', 'last_comment')
    op.drop_column('resource', 'deadline_week')
    op.drop_column('resource', 'num_comments')
    op.drop_column('resource', 'comments')
    op.drop_column('resource', 'course_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource', sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('resource', sa.Column('comments', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('resource', sa.Column('num_comments', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('resource', sa.Column('deadline_week', sa.VARCHAR(length=140), autoincrement=False, nullable=True))
    op.add_column('resource', sa.Column('last_comment', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('resource', 'creator')
    op.drop_column('resource', 'folder')
    op.create_table('course',
    sa.Column('course_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('course_name', sa.VARCHAR(length=140), autoincrement=False, nullable=True),
    sa.Column('maintainer', sa.VARCHAR(length=140), autoincrement=False, nullable=True),
    sa.Column('maintainer_email', sa.VARCHAR(length=140), autoincrement=False, nullable=True),
    sa.Column('course_institute', sa.VARCHAR(length=140), autoincrement=False, nullable=True),
    sa.Column('course_institute_id', sa.VARCHAR(length=140), autoincrement=False, nullable=True),
    sa.Column('course_institute_english', sa.VARCHAR(length=140), autoincrement=False, nullable=True),
    sa.Column('discord_channel_id', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('discord_invite', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('show_scans', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('updating_status', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('course_id', name='course_pkey')
    )
    # ### end Alembic commands ###
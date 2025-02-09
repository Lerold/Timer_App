"""Initial migration.

Revision ID: ca23ca39ffcf
Revises: 
Create Date: 2024-10-23 14:49:09.547901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca23ca39ffcf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timer_id', sa.Integer(), nullable=False),
    sa.Column('current_date', sa.String(length=20), nullable=False),
    sa.Column('current_time', sa.String(length=20), nullable=False),
    sa.Column('time_since_start', sa.String(length=20), nullable=False),
    sa.Column('tram_line_no', sa.String(length=10), nullable=True),
    sa.Column('tram_name', sa.String(length=100), nullable=True),
    sa.Column('direction', sa.String(length=100), nullable=True),
    sa.Column('rfid_tag', sa.String(length=100), nullable=True),
    sa.Column('switch_direction', sa.String(length=20), nullable=True),
    sa.Column('free_notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['timer_id'], ['timer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entry')
    op.drop_table('timer')
    # ### end Alembic commands ###

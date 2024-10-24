"""create task table

Revision ID: 0628408778cc
Revises: eb863f3e73fd
Create Date: 2024-10-22 15:58:16.583205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0628408778cc'
down_revision: Union[str, None] = 'eb863f3e73fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('responsible_id', sa.Integer(), nullable=False),
    sa.Column('watchers', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('performers', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('deadline', sa.Date(), nullable=False),
    sa.Column('status', sa.Enum('OPEN', 'IN_PROGRESS', 'CLOSED', name='taskstatus'), nullable=False),
    sa.Column('estimated_time_hours', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['employee.id'], ),
    sa.ForeignKeyConstraint(['responsible_id'], ['employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    # ### end Alembic commands ###

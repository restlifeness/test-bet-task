"""initial migrations

Revision ID: 98956928638c
Revises: 
Create Date: 2024-08-05 00:32:19.243737

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98956928638c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('external_events',
    sa.Column('external_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False, comment='Event name'),
    sa.Column('odds', sa.Numeric(precision=10, scale=2), nullable=False, comment='Event odds'),
    sa.Column('deadline', sa.DateTime(timezone=True), nullable=False, comment='Event deadline'),
    sa.Column('status', sa.Enum('OPEN', 'FIRST_TEAM_WIN', 'SECOND_TEAM_WIN', name='externaleventstatus'), nullable=False, comment='Event status'),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_external_events_external_id'), 'external_events', ['external_id'], unique=True)
    op.create_table('bets',
    sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=False, comment='Bet amount'),
    sa.Column('status', sa.Enum('PLACED', 'WON', 'LOST', name='betstatus'), nullable=False),
    sa.Column('external_event_id', sa.Integer(), nullable=False, comment='External event id'),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['external_event_id'], ['external_events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bets')
    op.drop_index(op.f('ix_external_events_external_id'), table_name='external_events')
    op.drop_table('external_events')
    # ### end Alembic commands ###
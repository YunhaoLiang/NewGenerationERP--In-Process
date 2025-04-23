"""create budgets table

Revision ID: 2025_04_22_1917
Revises: 3f54b58a01f8
Create Date: 2025-04-22 19:17:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2025_04_22_1917'
down_revision = '3f54b58a01f8'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('budgets',
        sa.Column('budget_id', sa.Integer(), nullable=False),
        sa.Column('department', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('period_start', sa.DateTime(), nullable=False),
        sa.Column('period_end', sa.DateTime(), nullable=False),
        sa.Column('actual_amount', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('budget_id')
    )
    op.create_index(op.f('ix_budgets_budget_id'), 'budgets', ['budget_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_budgets_budget_id'), table_name='budgets')
    op.drop_table('budgets') 
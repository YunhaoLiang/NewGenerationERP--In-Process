"""update enum types

Revision ID: 2025_04_19_1208
Revises: 2025_04_19_1207
Create Date: 2025-04-19 12:08:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2025_04_19_1208'
down_revision = '2025_04_19_1207'
branch_labels = None
depends_on = None

def upgrade():
    # 创建枚举类型
    op.execute('CREATE TYPE accounttype AS ENUM (\'asset\', \'liability\', \'equity\', \'revenue\', \'expense\')')
    op.execute('CREATE TYPE transactiontype AS ENUM (\'income\', \'expense\', \'transfer\')')

    # 创建财务相关表
    op.create_table('financial_accounts',
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('account_name', sa.String(100), nullable=False),
        sa.Column('account_type', sa.String(20), nullable=False),
        sa.Column('balance', sa.Float(), default=0.0),
        sa.Column('currency', sa.String(10), default='CNY'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('account_id')
    )
    op.create_index(op.f('ix_financial_accounts_account_id'), 'financial_accounts', ['account_id'], unique=False)

    op.create_table('transactions',
        sa.Column('transaction_id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=True),
        sa.Column('transaction_type', sa.String(20), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('transaction_date', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['financial_accounts.account_id'], ),
        sa.PrimaryKeyConstraint('transaction_id')
    )
    op.create_index(op.f('ix_transactions_transaction_id'), 'transactions', ['transaction_id'], unique=False)

    # 修改列类型
    op.alter_column('financial_accounts', 'account_type',
        type_=sa.Enum('asset', 'liability', 'equity', 'revenue', 'expense', name='accounttype'),
        postgresql_using='account_type::accounttype'
    )

    op.alter_column('transactions', 'transaction_type',
        type_=sa.Enum('income', 'expense', 'transfer', name='transactiontype'),
        postgresql_using='transaction_type::transactiontype'
    )

def downgrade():
    # 修改回原来的列类型
    op.alter_column('financial_accounts', 'account_type',
        type_=sa.String(20),
        postgresql_using='account_type::text'
    )

    op.alter_column('transactions', 'transaction_type',
        type_=sa.String(20),
        postgresql_using='transaction_type::text'
    )

    # 删除表
    op.drop_index(op.f('ix_transactions_transaction_id'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_financial_accounts_account_id'), table_name='financial_accounts')
    op.drop_table('financial_accounts')

    # 删除枚举类型
    op.execute('DROP TYPE accounttype')
    op.execute('DROP TYPE transactiontype') 
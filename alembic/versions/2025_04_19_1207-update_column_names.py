"""update column names

Revision ID: 2025_04_19_1207
Revises: 2025_04_19_1206
Create Date: 2025-04-19 12:07:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2025_04_19_1207'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 创建表
    op.create_table('users',
        sa.Column('用户id', sa.Integer(), nullable=False),
        sa.Column('用户名', sa.String(50), nullable=False),
        sa.Column('密码', sa.String(255), nullable=False),
        sa.Column('邮箱', sa.String(100), nullable=False),
        sa.Column('角色', sa.String(20), nullable=False),
        sa.Column('创建时间', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('用户id')
    )
    op.create_index(op.f('ix_users_用户id'), 'users', ['用户id'], unique=False)

    op.create_table('products',
        sa.Column('产品id', sa.Integer(), nullable=False),
        sa.Column('产品名称', sa.String(100), nullable=False),
        sa.Column('描述', sa.String(), nullable=True),
        sa.Column('单价', sa.Numeric(10, 2), nullable=False),
        sa.Column('类别', sa.String(50), nullable=True),
        sa.Column('创建时间', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('产品id')
    )
    op.create_index(op.f('ix_products_产品id'), 'products', ['产品id'], unique=False)

    op.create_table('suppliers',
        sa.Column('供应商id', sa.Integer(), nullable=False),
        sa.Column('供应商名称', sa.String(100), nullable=False),
        sa.Column('联系人', sa.String(100), nullable=True),
        sa.Column('邮箱', sa.String(100), nullable=True),
        sa.Column('电话', sa.String(20), nullable=True),
        sa.Column('地址', sa.String(), nullable=True),
        sa.Column('创建时间', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('供应商id')
    )
    op.create_index(op.f('ix_suppliers_供应商id'), 'suppliers', ['供应商id'], unique=False)

    op.create_table('inventory',
        sa.Column('库存id', sa.Integer(), nullable=False),
        sa.Column('产品id', sa.Integer(), nullable=True),
        sa.Column('数量', sa.Integer(), nullable=False),
        sa.Column('位置', sa.String(50), nullable=True),
        sa.Column('最后更新时间', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['产品id'], ['products.产品id'], ),
        sa.PrimaryKeyConstraint('库存id')
    )
    op.create_index(op.f('ix_inventory_库存id'), 'inventory', ['库存id'], unique=False)

    op.create_table('orders',
        sa.Column('订单id', sa.Integer(), nullable=False),
        sa.Column('用户id', sa.Integer(), nullable=True),
        sa.Column('产品id', sa.Integer(), nullable=True),
        sa.Column('数量', sa.Integer(), nullable=False),
        sa.Column('总金额', sa.Numeric(12, 2), nullable=False),
        sa.Column('状态', sa.String(20), nullable=False),
        sa.Column('创建时间', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['产品id'], ['products.产品id'], ),
        sa.ForeignKeyConstraint(['用户id'], ['users.用户id'], ),
        sa.PrimaryKeyConstraint('订单id')
    )
    op.create_index(op.f('ix_orders_订单id'), 'orders', ['订单id'], unique=False)

    # 修改列名
    op.alter_column('users', '用户id', new_column_name='user_id')
    op.alter_column('users', '用户名', new_column_name='username')
    op.alter_column('users', '密码', new_column_name='password')
    op.alter_column('users', '邮箱', new_column_name='email')
    op.alter_column('users', '角色', new_column_name='role')
    op.alter_column('users', '创建时间', new_column_name='created_at')

    op.alter_column('products', '产品id', new_column_name='product_id')
    op.alter_column('products', '产品名称', new_column_name='product_name')
    op.alter_column('products', '描述', new_column_name='description')
    op.alter_column('products', '单价', new_column_name='unit_price')
    op.alter_column('products', '类别', new_column_name='category')
    op.alter_column('products', '创建时间', new_column_name='created_at')

    op.alter_column('inventory', '库存id', new_column_name='inventory_id')
    op.alter_column('inventory', '产品id', new_column_name='product_id')
    op.alter_column('inventory', '数量', new_column_name='quantity')
    op.alter_column('inventory', '位置', new_column_name='location')
    op.alter_column('inventory', '最后更新时间', new_column_name='last_updated')

    op.alter_column('orders', '订单id', new_column_name='order_id')
    op.alter_column('orders', '用户id', new_column_name='user_id')
    op.alter_column('orders', '产品id', new_column_name='product_id')
    op.alter_column('orders', '数量', new_column_name='quantity')
    op.alter_column('orders', '总金额', new_column_name='total_amount')
    op.alter_column('orders', '状态', new_column_name='status')
    op.alter_column('orders', '创建时间', new_column_name='created_at')

    op.alter_column('suppliers', '供应商id', new_column_name='supplier_id')
    op.alter_column('suppliers', '供应商名称', new_column_name='supplier_name')
    op.alter_column('suppliers', '联系人', new_column_name='contact_person')
    op.alter_column('suppliers', '邮箱', new_column_name='email')
    op.alter_column('suppliers', '电话', new_column_name='phone')
    op.alter_column('suppliers', '地址', new_column_name='address')
    op.alter_column('suppliers', '创建时间', new_column_name='created_at')

def downgrade():
    # 修改回原来的列名
    op.alter_column('users', 'user_id', new_column_name='用户id')
    op.alter_column('users', 'username', new_column_name='用户名')
    op.alter_column('users', 'password', new_column_name='密码')
    op.alter_column('users', 'email', new_column_name='邮箱')
    op.alter_column('users', 'role', new_column_name='角色')
    op.alter_column('users', 'created_at', new_column_name='创建时间')

    op.alter_column('products', 'product_id', new_column_name='产品id')
    op.alter_column('products', 'product_name', new_column_name='产品名称')
    op.alter_column('products', 'description', new_column_name='描述')
    op.alter_column('products', 'unit_price', new_column_name='单价')
    op.alter_column('products', 'category', new_column_name='类别')
    op.alter_column('products', 'created_at', new_column_name='创建时间')

    op.alter_column('inventory', 'inventory_id', new_column_name='库存id')
    op.alter_column('inventory', 'product_id', new_column_name='产品id')
    op.alter_column('inventory', 'quantity', new_column_name='数量')
    op.alter_column('inventory', 'location', new_column_name='位置')
    op.alter_column('inventory', 'last_updated', new_column_name='最后更新时间')

    op.alter_column('orders', 'order_id', new_column_name='订单id')
    op.alter_column('orders', 'user_id', new_column_name='用户id')
    op.alter_column('orders', 'product_id', new_column_name='产品id')
    op.alter_column('orders', 'quantity', new_column_name='数量')
    op.alter_column('orders', 'total_amount', new_column_name='总金额')
    op.alter_column('orders', 'status', new_column_name='状态')
    op.alter_column('orders', 'created_at', new_column_name='创建时间')

    op.alter_column('suppliers', 'supplier_id', new_column_name='供应商id')
    op.alter_column('suppliers', 'supplier_name', new_column_name='供应商名称')
    op.alter_column('suppliers', 'contact_person', new_column_name='联系人')
    op.alter_column('suppliers', 'email', new_column_name='邮箱')
    op.alter_column('suppliers', 'phone', new_column_name='电话')
    op.alter_column('suppliers', 'address', new_column_name='地址')
    op.alter_column('suppliers', 'created_at', new_column_name='创建时间')

    # 删除表
    op.drop_index(op.f('ix_orders_订单id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_inventory_库存id'), table_name='inventory')
    op.drop_table('inventory')
    op.drop_index(op.f('ix_suppliers_供应商id'), table_name='suppliers')
    op.drop_table('suppliers')
    op.drop_index(op.f('ix_products_产品id'), table_name='products')
    op.drop_table('products')
    op.drop_index(op.f('ix_users_用户id'), table_name='users')
    op.drop_table('users') 
from sqlalchemy.orm import Session
from src.models.models import User, Product, Order, Inventory, FinancialAccount
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

# 测试数据库配置
TEST_DB_CONFIG = {
    "host": os.getenv("TEST_DB_HOST", "localhost"),
    "port": int(os.getenv("TEST_DB_PORT", 5432)),
    "database": os.getenv("TEST_DB_NAME", "erp_system_test"),
    "user": os.getenv("TEST_DB_USER", "postgres"),
    "password": os.getenv("TEST_DB_PASSWORD", "postgres123")
}

def clear_test_data(db: Session):
    """清除测试数据"""
    try:
        logger.info("清除旧的测试数据...")
        db.query(Order).delete()
        db.query(Inventory).delete()
        db.query(Product).delete()
        db.query(User).delete()
        db.query(FinancialAccount).delete()
        db.commit()
        logger.info("旧数据清除完成")
    except Exception as e:
        logger.error(f"清除数据时出错: {str(e)}")
        db.rollback()
        raise

def init_test_data(db: Session):
    """初始化测试数据"""
    try:
        # 清除旧数据
        clear_test_data(db)
        
        # 创建测试用户
        test_user = User(
            username="test_user",
            email="test@example.com",
            password="test_password",
            role="customer"
        )
        db.add(test_user)
        db.flush()  # 获取user_id
        
        # 创建测试产品
        products = [
            Product(
                product_name="高性能工作站",
                unit_price=15000.0,
                description="Intel i9, 32GB RAM, 1TB SSD, RTX 4080",
                category="computer"
            ),
            Product(
                product_name="商务办公本 Pro",
                unit_price=8000.0,
                description="Intel i7, 16GB RAM, 512GB SSD",
                category="laptop"
            )
        ]
        db.bulk_save_objects(products)
        db.flush()  # 获取product_ids
        
        # 查询刚创建的产品
        created_products = db.query(Product).all()
        
        # 创建库存记录
        for product in created_products:
            inventory = Inventory(
                product_id=product.product_id,
                quantity=100,
                location="主仓库",
                last_updated=datetime.now()
            )
            db.add(inventory)
        
        # 创建财务账户
        accounts = [
            FinancialAccount(
                account_name="主营业务账户",
                account_type="asset",
                balance=1000000.0,
                currency="CNY"
            ),
            FinancialAccount(
                account_name="运营支出账户",
                account_type="expense",
                balance=500000.0,
                currency="CNY"
            )
        ]
        db.bulk_save_objects(accounts)
        
        # 提交所有更改
        db.commit()
        
        logger.info("测试数据初始化完成")
        return {
            "user_id": test_user.user_id,
            "products": {p.product_name: p.product_id for p in created_products}
        }
        
    except Exception as e:
        logger.error(f"初始化测试数据时出错: {str(e)}")
        db.rollback()
        raise 
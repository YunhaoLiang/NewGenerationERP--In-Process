import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import SessionLocal
from src.models.models import User, Product, Inventory, Order, Supplier

def test_models():
    try:
        # 创建数据库会话
        db = SessionLocal()
        
        # 测试查询用户
        users = db.query(User).all()
        print("\n用户列表：")
        for user in users:
            print(f"用户ID: {user.用户ID}, 用户名: {user.用户名}, 角色: {user.角色}")
        
        # 测试查询产品
        products = db.query(Product).all()
        print("\n产品列表：")
        for product in products:
            print(f"产品ID: {product.产品ID}, 产品名称: {product.产品名称}, 单价: {product.单价}")
        
        # 测试查询库存
        inventory = db.query(Inventory).join(Product).all()
        print("\n库存列表：")
        for item in inventory:
            print(f"产品: {item.product.产品名称}, 数量: {item.数量}, 位置: {item.仓库位置}")
        
        # 测试查询订单
        orders = db.query(Order).join(User).join(Product).all()
        print("\n订单列表：")
        for order in orders:
            print(f"订单ID: {order.订单ID}, 用户: {order.user.用户名}, 产品: {order.product.产品名称}, 金额: {order.总金额}")
            
    except Exception as e:
        print(f"测试失败：{str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    test_models() 
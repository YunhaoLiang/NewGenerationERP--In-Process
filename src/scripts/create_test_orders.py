import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import SessionLocal
from src.models.models import Order, Product, User, Inventory
from datetime import datetime
from decimal import Decimal

def create_test_orders():
    """创建测试订单数据"""
    db = SessionLocal()
    try:
        # 获取所有用户和产品
        users = db.query(User).all()
        products = db.query(Product).all()
        
        if not users or not products:
            print("请先运行create_test_data.py创建基础数据")
            return
            
        # 创建一些测试订单
        orders = [
            {
                "user_id": users[2].user_id,  # sales1
                "product_id": products[0].product_id,  # ThinkPad X1
                "quantity": 2
            },
            {
                "user_id": users[3].user_id,  # sales2
                "product_id": products[1].product_id,  # Dell XPS
                "quantity": 1
            },
            {
                "user_id": users[2].user_id,  # sales1
                "product_id": products[2].product_id,  # MacBook Pro
                "quantity": 3
            },
            {
                "user_id": users[3].user_id,  # sales2
                "product_id": products[3].product_id,  # Surface Pro
                "quantity": 2
            },
            {
                "user_id": users[2].user_id,  # sales1
                "product_id": products[4].product_id,  # ASUS ZenBook
                "quantity": 1
            }
        ]
        
        for order_data in orders:
            # 检查库存
            inventory = db.query(Inventory).filter(Inventory.product_id == order_data["product_id"]).first()
            if not inventory or inventory.quantity < order_data["quantity"]:
                print(f"产品 {order_data['product_id']} 库存不足")
                continue
                
            # 获取产品价格
            product = db.query(Product).filter(Product.product_id == order_data["product_id"]).first()
            total_amount = product.unit_price * order_data["quantity"]
            
            # 创建订单
            new_order = Order(
                user_id=order_data["user_id"],
                product_id=order_data["product_id"],
                quantity=order_data["quantity"],
                total_amount=total_amount,
                status="created",
                created_at=datetime.now()
            )
            
            # 更新库存
            inventory.quantity -= order_data["quantity"]
            
            # 保存到数据库
            db.add(new_order)
            db.commit()
            print(f"创建订单成功：用户 {order_data['user_id']} 购买了 {order_data['quantity']} 件产品 {order_data['product_id']}")
            
    except Exception as e:
        print(f"创建订单时出错：{str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_orders() 
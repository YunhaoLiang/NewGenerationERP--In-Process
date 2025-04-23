from sqlalchemy.orm import Session
from src.models.models import Order, Product, User
from typing import List, Optional
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderDAO:
    """订单数据访问对象"""
    
    @staticmethod
    async def create_order(db: Session, user_id: int, product_id: int, quantity: int, total_amount: float) -> Order:
        """创建新订单
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            product_id: 产品ID
            quantity: 数量
            total_amount: 总金额
            
        Returns:
            Order: 创建的订单对象
        """
        try:
            logger.info(f"开始创建订单: user_id={user_id}, product_id={product_id}, quantity={quantity}")
            
            # 检查用户是否存在
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                logger.error(f"用户不存在: user_id={user_id}")
                raise ValueError(f"用户不存在: {user_id}")
            
            # 检查产品是否存在
            product = db.query(Product).filter(Product.product_id == product_id).first()
            if not product:
                logger.error(f"产品不存在: product_id={product_id}")
                raise ValueError(f"产品不存在: {product_id}")
            
            # 创建订单
            order = Order(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                total_amount=total_amount,
                status="created",
                created_at=datetime.now()
            )
            
            logger.info("添加订单到数据库会话")
            db.add(order)
            
            logger.info("提交事务")
            db.commit()
            
            logger.info("刷新订单对象")
            db.refresh(order)
            
            logger.info(f"订单创建成功: order_id={order.order_id}")
            return order
            
        except Exception as e:
            logger.error(f"创建订单失败: {str(e)}")
            db.rollback()
            raise
    
    @staticmethod
    async def get_order(db: Session, order_id: int) -> Optional[Order]:
        """获取订单
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            
        Returns:
            Optional[Order]: 订单对象，如果不存在则返回None
        """
        try:
            logger.info(f"查询订单: order_id={order_id}")
            order = db.query(Order).filter(Order.order_id == order_id).first()
            if order:
                logger.info("订单查询成功")
            else:
                logger.info("订单不存在")
            return order
        except Exception as e:
            logger.error(f"查询订单失败: {str(e)}")
            raise
    
    @staticmethod
    async def get_user_orders(db: Session, user_id: int) -> List[Order]:
        """获取用户的所有订单
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            List[Order]: 订单列表
        """
        try:
            logger.info(f"查询用户订单: user_id={user_id}")
            orders = db.query(Order).filter(Order.user_id == user_id).all()
            logger.info(f"查询到 {len(orders)} 个订单")
            return orders
        except Exception as e:
            logger.error(f"查询用户订单失败: {str(e)}")
            raise
    
    @staticmethod
    async def update_order_status(db: Session, order_id: int, status: str) -> Optional[Order]:
        """更新订单状态
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            status: 新状态
            
        Returns:
            Optional[Order]: 更新后的订单对象，如果订单不存在则返回None
        """
        try:
            logger.info(f"更新订单状态: order_id={order_id}, status={status}")
            order = db.query(Order).filter(Order.order_id == order_id).first()
            if order:
                order.status = status
                db.commit()
                db.refresh(order)
                logger.info("订单状态更新成功")
            else:
                logger.info("订单不存在")
            return order
        except Exception as e:
            logger.error(f"更新订单状态失败: {str(e)}")
            db.rollback()
            raise 
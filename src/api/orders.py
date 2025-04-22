from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from src.config.database import get_db
from src.models.order import Order, OrderItem
from src.models.product import Product
from pydantic import BaseModel
import json

router = APIRouter()

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    specifications: dict

class OrderCreate(BaseModel):
    customer_name: str
    shipping_address: str
    delivery_date: datetime
    items: List[OrderItemCreate]
    specifications: Optional[dict] = None

@router.post("/orders/")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # 生成订单号
    order_no = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # 计算总金额
    total_amount = sum(item.quantity * item.unit_price for item in order.items)
    
    # 创建订单
    db_order = Order(
        order_no=order_no,
        customer_name=order.customer_name,
        total_amount=total_amount,
        status="pending_payment",
        shipping_address=order.shipping_address,
        delivery_date=order.delivery_date,
        specifications=order.specifications
    )
    db.add(db_order)
    db.flush()  # 获取订单ID
    
    # 创建订单项
    for item in order.items:
        # 检查产品是否存在
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        # 检查库存
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        
        # 创建订单项
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            specifications=item.specifications
        )
        db.add(db_item)
        
        # 更新库存
        product.stock -= item.quantity
    
    try:
        db.commit()
        return {"order_no": order_no, "message": "订单创建成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 
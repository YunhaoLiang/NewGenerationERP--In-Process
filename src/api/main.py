import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from src.core.orchestrator import LLMOrchestrator
from src.agents.order_agent import OrderAgent
from src.agents.planning_agent import PlanningAgent
from src.agents.base_agent import BaseAgent
from fastapi.responses import RedirectResponse
from src.config.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from src.models.models import Order, Product, User, Inventory
from datetime import datetime
from . import finance, supplier, inventory, user, product

app = FastAPI(title="New Generation ERP")

# 添加根路径路由
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# 注册所有路由
app.include_router(finance.router)
app.include_router(supplier.router)
app.include_router(inventory.router)
app.include_router(user.router)
app.include_router(product.router)

# 初始化组件
orchestrator = LLMOrchestrator()
order_agent = OrderAgent()
planning_agent = PlanningAgent()

# 订单相关的Pydantic模型
class OrderCreate(BaseModel):
    """创建订单的请求模型"""
    user_id: int
    product_id: int
    quantity: int

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class OrderResponse(BaseModel):
    """订单响应模型"""
    order_id: int
    user_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: str
    created_at: datetime

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
        orm_mode = True

class Instruction(BaseModel):
    """业务指令模型"""
    text: str
    parameters: Dict[str, Any] = {}

@app.post("/process_instruction")
async def process_instruction(instruction: Instruction):
    """处理业务指令
    
    Args:
        instruction: 业务指令
        
    Returns:
        Dict: 处理结果
    """
    try:
        print("\n=== 收到新的指令 ===")
        print(f"指令内容: {instruction.text}")
        print(f"指令参数: {instruction.parameters}")
        
        # 使用编排器处理指令
        task = await orchestrator.process_instruction(instruction.text, instruction.parameters)
        print(f"\n=== 任务创建结果 ===")
        print(f"任务ID: {task.task_id}")
        print(f"任务类型: {task.task_type}")
        print(f"任务参数: {task.parameters}")
        
        # 根据任务类型调用相应的Agent
        if task.task_type == "order":
            result = await order_agent.process(task.parameters)
            print(f"\n=== 订单处理结果 ===")
            print(f"处理状态: {result.status}")
            print(f"订单数据: {result.data}")
            return result.dict()
        elif task.task_type == "planning":
            result = await planning_agent.process(task.parameters)
            print(f"\n=== 计划处理结果 ===")
            print(f"处理状态: {result.status}")
            print(f"计划数据: {result.data}")
            return result.dict()
        else:
            raise HTTPException(status_code=400, detail="Unsupported task type")
            
    except Exception as e:
        print(f"\n=== 处理出错 ===")
        print(f"错误信息: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent_status/{agent_id}")
async def get_agent_status(agent_id: str):
    """获取Agent状态
    
    Args:
        agent_id: Agent ID
        
    Returns:
        Dict: Agent状态
    """
    if agent_id == order_agent.agent_id:
        return order_agent.get_status()
    elif agent_id == planning_agent.agent_id:
        return planning_agent.get_status()
    else:
        raise HTTPException(status_code=404, detail="Agent not found")

# 订单CRUD API
@app.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """创建新订单"""
    try:
        # 检查用户是否存在
        user = db.query(User).filter(User.user_id == order.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        # 检查产品是否存在
        product = db.query(Product).filter(Product.product_id == order.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="产品不存在")

        # 检查库存
        inventory = db.query(Inventory).filter(Inventory.product_id == order.product_id).first()
        if not inventory or inventory.quantity < order.quantity:
            raise HTTPException(status_code=400, detail="库存不足")

        # 计算订单金额
        total_amount = product.unit_price * order.quantity

        # 创建订单
        new_order = Order(
            user_id=order.user_id,
            product_id=order.product_id,
            quantity=order.quantity,
            total_amount=total_amount,
            status='created',
            created_at=datetime.now()
        )

        # 更新库存
        inventory.quantity -= order.quantity

        # 保存到数据库
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return new_order

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders", response_model=List[OrderResponse])
async def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取订单列表"""
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders

@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """获取单个订单"""
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order

@app.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    """更新订单"""
    try:
        db_order = db.query(Order).filter(Order.order_id == order_id).first()
        if db_order is None:
            raise HTTPException(status_code=404, detail="订单不存在")

        # 检查用户是否存在
        user = db.query(User).filter(User.user_id == order.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        # 检查产品是否存在
        product = db.query(Product).filter(Product.product_id == order.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="产品不存在")

        # 检查库存
        inventory = db.query(Inventory).filter(Inventory.product_id == order.product_id).first()
        if not inventory or inventory.quantity < order.quantity:
            raise HTTPException(status_code=400, detail="库存不足")

        # 计算订单金额
        total_amount = product.unit_price * order.quantity

        # 更新订单
        db_order.user_id = order.user_id
        db_order.product_id = order.product_id
        db_order.quantity = order.quantity
        db_order.total_amount = total_amount
        db_order.created_at = datetime.now()

        # 更新库存
        inventory.quantity -= order.quantity

        db.commit()
        db.refresh(db_order)
        return db_order

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    """删除订单"""
    try:
        db_order = db.query(Order).filter(Order.order_id == order_id).first()
        if db_order is None:
            raise HTTPException(status_code=404, detail="订单不存在")

        # 恢复库存
        inventory = db.query(Inventory).filter(Inventory.product_id == db_order.product_id).first()
        if inventory:
            inventory.quantity += db_order.quantity

        db.delete(db_order)
        db.commit()
        return {"message": "订单已删除"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 更新数据库连接处理
@app.on_event("shutdown")
async def shutdown_event():
    """关闭数据库连接"""
    try:
        if hasattr(app, 'db') and app.db is not None:
            app.db.close()
    except Exception as e:
        print(f"关闭数据库连接时出错：{str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8082)

## 在项目根目录下运行
# cd C:\Users\Louis\Desktop\NewGenerationERP--In-Process
# python -m src.api.main
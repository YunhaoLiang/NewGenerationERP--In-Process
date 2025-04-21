from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal

from src.config.database import get_db
from src.models.models import Inventory, Product

router = APIRouter(prefix="/inventory", tags=["inventory"])

# Pydantic模型
class InventoryCreate(BaseModel):
    product_id: int
    quantity: int
    location: str

class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None
    location: Optional[str] = None

class InventoryResponse(BaseModel):
    inventory_id: int
    product_id: int
    quantity: int
    location: str
    last_updated: datetime
    
    class Config:
        orm_mode = True

class InventoryDetailResponse(InventoryResponse):
    product_name: str
    unit_price: Decimal
    total_value: Decimal

# API端点
@router.post("", response_model=InventoryResponse)
async def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    """创建库存记录"""
    # 检查产品是否存在
    product = db.query(Product).filter(Product.product_id == inventory.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    
    # 检查是否已存在该产品的库存记录
    existing = db.query(Inventory).filter(Inventory.product_id == inventory.product_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="该产品的库存记录已存在")
    
    db_inventory = Inventory(
        product_id=inventory.product_id,
        quantity=inventory.quantity,
        location=inventory.location,
        last_updated=datetime.now()
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@router.get("", response_model=List[InventoryDetailResponse])
async def get_inventory(
    skip: int = 0,
    limit: int = 100,
    location: Optional[str] = None,
    min_quantity: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取库存列表"""
    query = db.query(
        Inventory,
        Product.product_name,
        Product.unit_price,
        (Product.unit_price * Inventory.quantity).label('total_value')
    ).join(Product)
    
    if location:
        query = query.filter(Inventory.location == location)
    if min_quantity is not None:
        query = query.filter(Inventory.quantity >= min_quantity)
    
    results = query.offset(skip).limit(limit).all()
    
    # 转换为响应格式
    response = []
    for result in results:
        inventory_dict = {
            "inventory_id": result.Inventory.inventory_id,
            "product_id": result.Inventory.product_id,
            "quantity": result.Inventory.quantity,
            "location": result.Inventory.location,
            "last_updated": result.Inventory.last_updated,
            "product_name": result.product_name,
            "unit_price": result.unit_price,
            "total_value": result.total_value
        }
        response.append(inventory_dict)
    
    return response

@router.get("/{inventory_id}", response_model=InventoryDetailResponse)
async def get_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    """获取库存详情"""
    result = db.query(
        Inventory,
        Product.product_name,
        Product.unit_price,
        (Product.unit_price * Inventory.quantity).label('total_value')
    ).join(Product).filter(Inventory.inventory_id == inventory_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    
    return {
        "inventory_id": result.Inventory.inventory_id,
        "product_id": result.Inventory.product_id,
        "quantity": result.Inventory.quantity,
        "location": result.Inventory.location,
        "last_updated": result.Inventory.last_updated,
        "product_name": result.product_name,
        "unit_price": result.unit_price,
        "total_value": result.total_value
    }

@router.put("/{inventory_id}", response_model=InventoryResponse)
async def update_inventory(
    inventory_id: int,
    inventory: InventoryUpdate,
    db: Session = Depends(get_db)
):
    """更新库存信息"""
    db_inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if not db_inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    
    if inventory.quantity is not None:
        db_inventory.quantity = inventory.quantity
    if inventory.location is not None:
        db_inventory.location = inventory.location
    
    db_inventory.last_updated = datetime.now()
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@router.delete("/{inventory_id}")
async def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    """删除库存记录"""
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    
    db.delete(inventory)
    db.commit()
    return {"message": "库存记录已删除"}

# 库存调整API
class InventoryAdjustment(BaseModel):
    quantity_change: int  # 正数表示入库，负数表示出库
    reason: str

@router.post("/{inventory_id}/adjust", response_model=InventoryResponse)
async def adjust_inventory(
    inventory_id: int,
    adjustment: InventoryAdjustment,
    db: Session = Depends(get_db)
):
    """调整库存数量"""
    db_inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if not db_inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    
    new_quantity = db_inventory.quantity + adjustment.quantity_change
    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="库存不足")
    
    db_inventory.quantity = new_quantity
    db_inventory.last_updated = datetime.now()
    
    db.commit()
    db.refresh(db_inventory)
    return db_inventory 
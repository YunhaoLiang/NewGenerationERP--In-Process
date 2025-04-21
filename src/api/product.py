from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, condecimal
from decimal import Decimal

from src.config.database import get_db
from src.models.models import Product, Inventory

router = APIRouter(prefix="/products", tags=["products"])

# Pydantic模型
class ProductCreate(BaseModel):
    product_name: str
    description: Optional[str] = None
    unit_price: condecimal(max_digits=10, decimal_places=2)
    category: str

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    unit_price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    category: Optional[str] = None

class ProductResponse(BaseModel):
    product_id: int
    product_name: str
    description: Optional[str]
    unit_price: Decimal
    category: str
    created_at: datetime

    class Config:
        orm_mode = True

class ProductDetailResponse(ProductResponse):
    inventory_quantity: Optional[int]
    inventory_location: Optional[str]

# API端点
@router.post("", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """创建产品"""
    # 检查产品名是否已存在
    existing = db.query(Product).filter(Product.product_name == product.product_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="产品名称已存在")
    
    db_product = Product(
        product_name=product.product_name,
        description=product.description,
        unit_price=product.unit_price,
        category=product.category,
        created_at=datetime.now()
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("", response_model=List[ProductDetailResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """获取产品列表"""
    query = db.query(
        Product,
        Inventory.quantity.label('inventory_quantity'),
        Inventory.location.label('inventory_location')
    ).outerjoin(Inventory)
    
    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.unit_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.unit_price <= max_price)
    
    results = query.offset(skip).limit(limit).all()
    
    # 转换为响应格式
    response = []
    for result in results:
        product_dict = {
            "product_id": result.Product.product_id,
            "product_name": result.Product.product_name,
            "description": result.Product.description,
            "unit_price": result.Product.unit_price,
            "category": result.Product.category,
            "created_at": result.Product.created_at,
            "inventory_quantity": result.inventory_quantity,
            "inventory_location": result.inventory_location
        }
        response.append(product_dict)
    
    return response

@router.get("/{product_id}", response_model=ProductDetailResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取产品详情"""
    result = db.query(
        Product,
        Inventory.quantity.label('inventory_quantity'),
        Inventory.location.label('inventory_location')
    ).outerjoin(Inventory).filter(Product.product_id == product_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="产品不存在")
    
    return {
        "product_id": result.Product.product_id,
        "product_name": result.Product.product_name,
        "description": result.Product.description,
        "unit_price": result.Product.unit_price,
        "category": result.Product.category,
        "created_at": result.Product.created_at,
        "inventory_quantity": result.inventory_quantity,
        "inventory_location": result.inventory_location
    }

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """更新产品信息"""
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="产品不存在")
    
    # 检查产品名是否已存在
    if product.product_name:
        existing = db.query(Product).filter(
            Product.product_name == product.product_name,
            Product.product_id != product_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="产品名称已存在")
        db_product.product_name = product.product_name
    
    if product.description is not None:
        db_product.description = product.description
    if product.unit_price is not None:
        db_product.unit_price = product.unit_price
    if product.category is not None:
        db_product.category = product.category
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """删除产品"""
    # 检查是否有关联的库存记录
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if inventory:
        raise HTTPException(status_code=400, detail="该产品有关联的库存记录，无法删除")
    
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    
    db.delete(product)
    db.commit()
    return {"message": "产品已删除"}

# 批量操作API
class ProductPriceUpdate(BaseModel):
    product_ids: List[int]
    price_change: float  # 正数表示涨价，负数表示降价
    change_type: str  # "amount" 或 "percentage"

@router.post("/batch/update-price")
async def batch_update_price(
    update: ProductPriceUpdate,
    db: Session = Depends(get_db)
):
    """批量更新产品价格"""
    products = db.query(Product).filter(Product.product_id.in_(update.product_ids)).all()
    if not products:
        raise HTTPException(status_code=404, detail="未找到指定的产品")
    
    updated_products = []
    for product in products:
        if update.change_type == "amount":
            new_price = product.unit_price + Decimal(str(update.price_change))
        else:  # percentage
            new_price = product.unit_price * (1 + Decimal(str(update.price_change)) / 100)
        
        if new_price < 0:
            raise HTTPException(status_code=400, detail=f"产品 {product.product_name} 的新价格不能为负数")
        
        product.unit_price = new_price
        updated_products.append({
            "product_id": product.product_id,
            "product_name": product.product_name,
            "old_price": product.unit_price - Decimal(str(update.price_change)) if update.change_type == "amount"
                        else product.unit_price / (1 + Decimal(str(update.price_change)) / 100),
            "new_price": new_price
        })
    
    db.commit()
    return {"message": "价格更新成功", "updated_products": updated_products} 
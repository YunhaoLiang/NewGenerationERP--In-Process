from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from src.config.database import get_db
from src.models.product import Product

router = APIRouter()

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    stock: int
    status: str = "active"
    specifications: Optional[dict] = None
    description: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    stock: int
    status: str
    specifications: Optional[dict]
    description: Optional[str]

    class Config:
        from_attributes = True

@router.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        category=product.category,
        price=product.price,
        stock=product.stock,
        status=product.status,
        specifications=product.specifications,
        description=product.description
    )
    db.add(db_product)
    
    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    return query.offset(skip).limit(limit).all() 
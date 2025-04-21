from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from src.config.database import get_db
from src.models.models import Supplier

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

# Pydantic模型
class SupplierCreate(BaseModel):
    supplier_name: str
    contact_person: str
    email: str
    phone: str
    address: Optional[str] = None

class SupplierResponse(BaseModel):
    supplier_id: int
    supplier_name: str
    contact_person: str
    email: str
    phone: str
    address: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

# API端点
@router.post("", response_model=SupplierResponse)
async def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """创建供应商"""
    db_supplier = Supplier(
        supplier_name=supplier.supplier_name,
        contact_person=supplier.contact_person,
        email=supplier.email,
        phone=supplier.phone,
        address=supplier.address,
        created_at=datetime.now()
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@router.get("", response_model=List[SupplierResponse])
async def get_suppliers(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取供应商列表"""
    query = db.query(Supplier)
    if name:
        query = query.filter(Supplier.supplier_name.ilike(f"%{name}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """获取供应商详情"""
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    return supplier

@router.put("/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(
    supplier_id: int,
    supplier: SupplierCreate,
    db: Session = Depends(get_db)
):
    """更新供应商信息"""
    db_supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    
    for field, value in supplier.dict().items():
        setattr(db_supplier, field, value)
    
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@router.delete("/{supplier_id}")
async def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """删除供应商"""
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    
    db.delete(supplier)
    db.commit()
    return {"message": "供应商已删除"} 
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
import hashlib

from src.config.database import get_db
from src.models.models import User

router = APIRouter(prefix="/users", tags=["users"])

# Pydantic模型
class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str

class UserUpdate(BaseModel):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        orm_mode = True

def hash_password(password: str) -> str:
    """对密码进行哈希处理"""
    return hashlib.sha256(password.encode()).hexdigest()

# API端点
@router.post("", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """创建用户"""
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查邮箱是否已存在
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    # 验证角色
    valid_roles = ["admin", "manager", "sales", "warehouse"]
    if user.role not in valid_roles:
        raise HTTPException(status_code=400, detail="无效的角色")
    
    # 创建用户
    db_user = User(
        username=user.username,
        password=hash_password(user.password),
        email=user.email,
        role=user.role,
        created_at=datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.offset(skip).limit(limit).all()

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """获取用户详情"""
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新密码
    if user.password:
        db_user.password = hash_password(user.password)
    
    # 更新邮箱
    if user.email:
        existing_email = db.query(User).filter(
            User.email == user.email,
            User.user_id != user_id
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="邮箱已存在")
        db_user.email = user.email
    
    # 更新角色
    if user.role:
        valid_roles = ["admin", "manager", "sales", "warehouse"]
        if user.role not in valid_roles:
            raise HTTPException(status_code=400, detail="无效的角色")
        db_user.role = user.role
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """删除用户"""
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db.delete(user)
    db.commit()
    return {"message": "用户已删除"}

# 用户认证API
class UserLogin(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    user_id: int
    username: str
    role: str
    token: str  # 实际项目中应该使用JWT

@router.post("/login", response_model=LoginResponse)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or db_user.password != hash_password(user.password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 这里应该生成JWT token，这里简单返回一个模拟token
    token = f"mock_token_{db_user.user_id}_{datetime.now().timestamp()}"
    
    return {
        "user_id": db_user.user_id,
        "username": db_user.username,
        "role": db_user.role,
        "token": token
    } 
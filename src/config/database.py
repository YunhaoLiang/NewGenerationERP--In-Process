from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接URL
DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/erp_system"
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 自动检测断开的连接
    pool_recycle=3600,   # 一小时后回收连接
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基本模型类
Base = declarative_base()

# 获取数据库会话的依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
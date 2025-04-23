from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from src.config.database import engine
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.get("/sales-trend")
async def get_sales_trend():
    try:
        with engine.connect() as conn:
            # 获取最近12个月的销售数据
            query = text("""
                SELECT 
                    DATE_TRUNC('month', o.created_at) as month,
                    SUM(oi.quantity * oi.unit_price) as total_sales
                FROM orders o
                JOIN order_items oi ON o.id = oi.order_id
                WHERE o.created_at >= NOW() - INTERVAL '12 months'
                GROUP BY DATE_TRUNC('month', o.created_at)
                ORDER BY month ASC
            """)
            result = conn.execute(query)
            sales_data = [{"month": row[0].strftime("%Y-%m"), "total_sales": float(row[1])} if row[1] else 
                         {"month": row[0].strftime("%Y-%m"), "total_sales": 0.0} 
                         for row in result]
            return sales_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/category-distribution")
async def get_category_distribution():
    try:
        with engine.connect() as conn:
            # 获取产品类别分布
            query = text("""
                SELECT 
                    p.category,
                    COUNT(*) as count,
                    SUM(oi.quantity * oi.unit_price) as total_sales
                FROM products p
                JOIN order_items oi ON p.id = oi.product_id
                GROUP BY p.category
                ORDER BY total_sales DESC
            """)
            result = conn.execute(query)
            category_data = [{"category": row[0] or "其他", 
                            "count": int(row[1]),
                            "total_sales": float(row[2])} 
                           for row in result]
            return category_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
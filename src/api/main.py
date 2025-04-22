from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.nlp import router as nlp_router
from src.api.orders import router as orders_router
from src.api.products import router as products_router
from src.config.database import engine
from sqlalchemy import text

app = FastAPI(title="ERP自然语言处理API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库表
def init_db():
    with engine.connect() as conn:
        # 删除现有表
        conn.execute(text("DROP TABLE IF EXISTS order_items"))
        conn.execute(text("DROP TABLE IF EXISTS orders"))
        conn.execute(text("DROP TABLE IF EXISTS products"))
        
        # 创建产品表
        conn.execute(text("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                category VARCHAR,
                price FLOAT,
                stock INTEGER,
                status VARCHAR,
                specifications JSON,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # 创建订单表
        conn.execute(text("""
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                order_no VARCHAR UNIQUE NOT NULL,
                customer_name VARCHAR NOT NULL,
                total_amount FLOAT,
                status VARCHAR,
                shipping_address TEXT,
                delivery_date TIMESTAMP,
                specifications JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # 创建订单项表
        conn.execute(text("""
            CREATE TABLE order_items (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
                product_id INTEGER REFERENCES products(id),
                quantity INTEGER,
                unit_price FLOAT,
                specifications JSON
            )
        """))
        
        conn.commit()

# 初始化数据库
init_db()

# 注册路由
app.include_router(nlp_router, prefix="/api/nlp", tags=["自然语言处理"])
app.include_router(orders_router, prefix="/api/orders", tags=["orders"])
app.include_router(products_router, prefix="/api/products", tags=["products"])

@app.get("/")
async def root():
    return {"message": "Welcome to ERP System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
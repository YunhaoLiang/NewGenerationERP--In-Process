import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent

# 加载环境变量
load_dotenv(project_root / '.env')

# 数据库配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "erp_system"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "")
}

async def init_db():
    """初始化数据库"""
    # 创建数据库连接池
    pool = await asyncpg.create_pool(**DB_CONFIG)
    
    try:
        async with pool.acquire() as conn:
            # 读取SQL文件
            sql_file = current_dir / 'migrations' / 'create_task_history_table.sql'
            if not sql_file.exists():
                raise FileNotFoundError(f"SQL文件不存在: {sql_file}")
                
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql = f.read()
            
            # 执行SQL
            await conn.execute(sql)
            print("数据库初始化完成")
            
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        raise e
        
    finally:
        await pool.close()

if __name__ == "__main__":
    asyncio.run(init_db()) 
import os
import sys
import psycopg2
from psycopg2 import OperationalError

# 设置系统编码
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def test_db_connection():
    print("环境变量:")
    print(f"DB_HOST: {os.getenv('DB_HOST', '未设置')}")
    print(f"DB_PORT: {os.getenv('DB_PORT', '未设置')}")
    print(f"DB_NAME: {os.getenv('DB_NAME', '未设置')}")
    print(f"DB_USER: {os.getenv('DB_USER', '未设置')}")
    print(f"DB_PASSWORD: {'已设置' if os.getenv('DB_PASSWORD') else '未设置'}")

    print("\n正在连接数据库...")
    
    try:
        # 构建连接参数
        conn_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        
        # 打印连接信息（不包含密码）
        print(f"连接信息: host={conn_params['host']}, port={conn_params['port']}, "
              f"database={conn_params['database']}, user={conn_params['user']}")
        
        # 尝试连接数据库
        conn = psycopg2.connect(**conn_params)
        print("数据库连接成功！")
        
        # 关闭连接
        conn.close()
        
    except OperationalError as e:
        print(f"\n数据库连接错误: {str(e)}")
        print("\n请检查以下内容：")
        print("1. 确保PostgreSQL服务正在运行")
        print("2. 检查数据库连接参数是否正确")
        print("3. 确认用户名和密码是否正确")
        print("4. 验证数据库是否存在")
    except Exception as e:
        print(f"\n其他错误: {str(e)}")
        print("\n请检查系统编码设置和数据库配置")

if __name__ == "__main__":
    test_db_connection() 
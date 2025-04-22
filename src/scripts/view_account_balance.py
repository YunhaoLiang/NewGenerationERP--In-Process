import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database import engine
from sqlalchemy import text
from tabulate import tabulate

def view_account_balance():
    """查看账户余额"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM vw_account_balance"))
            rows = result.fetchall()
            headers = result.keys()
            
            if rows:
                print("\n=== 财务账户余额报表 ===")
                print(tabulate(rows, headers=headers, tablefmt="grid"))
            else:
                print("没有找到账户数据")
    except Exception as e:
        print(f"查询账户余额时出错：{str(e)}")

if __name__ == "__main__":
    view_account_balance() 
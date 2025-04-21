import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy import text
from src.config.database import engine

def drop_enum(enum_name):
    try:
        with engine.connect() as conn:
            conn.execute(text(f'DROP TYPE IF EXISTS {enum_name} CASCADE'))
            conn.commit()
            print(f'已删除枚举类型：{enum_name}')
    except Exception as e:
        print(f'删除枚举类型 {enum_name} 时出错：{str(e)}')

if __name__ == '__main__':
    enums = [
        'accounttype',
        'transactiontype'
    ]
    
    for enum in enums:
        drop_enum(enum) 
import os
import sys

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将项目根目录添加到Python路径
sys.path.insert(0, current_dir)

# 导入并运行main.py
from src.api.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080) 
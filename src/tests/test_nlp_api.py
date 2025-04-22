import pytest
import httpx
import logging
import json
from fastapi.testclient import TestClient
from src.api.main import app

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nlp_api_test.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 创建测试客户端
client = TestClient(app)

def test_nlp_process():
    """测试 NLP 处理接口"""
    try:
        # 准备测试数据
        test_data = {
            "text": "创建新订单",
            "requireAgents": False
        }
        
        logger.info(f"发送测试请求: {test_data}")
        
        # 发送请求
        response = client.post("/api/nlp/process", json=test_data)
        
        # 记录响应
        logger.info(f"收到响应状态码: {response.status_code}")
        logger.info(f"响应内容: {response.text}")
        
        # 断言响应
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == "success"
        
        return {
            "status": "测试成功",
            "request": test_data,
            "response": response_data
        }
        
    except Exception as e:
        logger.error(f"测试失败: {str(e)}", exc_info=True)
        return {
            "status": "测试失败",
            "error": str(e),
            "request": test_data if 'test_data' in locals() else None
        }

if __name__ == "__main__":
    """直接运行测试"""
    print("开始测试 NLP API...")
    result = test_nlp_process()
    print(json.dumps(result, ensure_ascii=False, indent=2)) 
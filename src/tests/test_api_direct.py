import requests
import json

def test_api():
    url = "http://localhost:8001/api/nlp/process"
    headers = {"Content-Type": "application/json"}
    data = {
        "text": "创建新订单",
        "requireAgents": False
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    test_api() 
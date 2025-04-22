import requests
import json

# 产品数据
product_data = {
    "name": "高性能商务电脑",
    "category": "electronics",
    "price": 15999.00,
    "stock": 1000,
    "status": "active",
    "specifications": {
        "processor": "Intel i9",
        "memory": "32GB",
        "storage": "1TB SSD",
        "graphics": "NVIDIA RTX 4080"
    },
    "description": "高性能商务电脑，配备Intel i9处理器、32GB内存、1TB SSD和NVIDIA RTX 4080显卡"
}

# 发送POST请求
response = requests.post(
    "http://localhost:8001/api/products/",
    json=product_data
)

# 打印响应
print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), ensure_ascii=False, indent=2)) 
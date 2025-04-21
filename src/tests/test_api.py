import requests
import json

def test_create_order():
    url = "http://127.0.0.1:8082/orders"
    headers = {"Content-Type": "application/json"}
    data = {
        "user_id": 1,
        "product_id": 1,
        "quantity": 2
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_create_order() 
import requests
import json

# Тест add метода
response = requests.post(
    'http://localhost:5000/rpc',
    json={"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 1}
)
print("Add result:", response.json())

# Тест get_user метода
response = requests.post(
    'http://localhost:5000/rpc', 
    json={"jsonrpc": "2.0", "method": "get_user", "params": [2], "id": 2}
)
print("Get user result:", response.json())
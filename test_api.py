import requests
import json

payload = {
    "query": "What is the capital of France?",
    "tools": [{"name": "get_stock_price", "description": "Get stock price", "parameters": {"type": "object", "properties": {"symbol": {"type": "string"}}, "required": ["symbol"]}}]
}
try:
    response = requests.post("https://scalding-creme-broiling.ngrok-free.dev/generate", json=payload)
    print("Status:", response.status_code)
    print("Body:", response.text)
except Exception as e:
    print("Error:", e)

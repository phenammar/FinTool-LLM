import os
import requests

def get_stock_price(symbol: str) -> dict:
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise ValueError("ALPHA_VANTAGE_API_KEY is not set.")
        
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()
    
    if "Information" in data:
        raise RuntimeError(f"Alpha Vantage Error: {data['Information']}")
    if "Note" in data:
        raise RuntimeError(f"Alpha Vantage Rate Limit: {data['Note']}")
        
    return data

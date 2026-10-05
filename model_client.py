import os
import requests
import json
from prompt import construct_prompt

def call_model_api(query: str) -> dict:
    """
    Calls the remote Model API (or mock) and returns the tool call JSON.
    """
    is_mock = os.getenv("MOCK_MODEL", "false").lower() == "true"
    
    if is_mock:
        return _mock_model_response(query)
        
    model_api_url = os.getenv("MODEL_API_URL")
    if not model_api_url:
        raise ValueError("MODEL_API_URL environment variable is not set.")
        
    prompt = construct_prompt(query)
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(model_api_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Assume response format is {"response": "{...JSON string...}"}
        # or directly {"name": "...", "arguments": {...}}
        model_response = data.get("response", "")
        if isinstance(model_response, dict):
            return model_response
            
        return json.loads(model_response)
        
    except requests.exceptions.Timeout:
        raise RuntimeError("Model API request timed out.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to connect to Model API: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError("Model returned invalid JSON format.")

def _mock_model_response(query: str) -> dict:
    """
    Simple rule-based mock for testing without a real LLM.
    """
    query_lower = query.lower()
    
    if "news" in query_lower:
        return {"name": "get_company_news", "arguments": {"symbol": "AAPL"}}
    elif "history" in query_lower or "historical" in query_lower:
        return {"name": "get_historical_prices", "arguments": {"symbol": "AAPL"}}
    elif "info" in query_lower or "about" in query_lower:
        return {"name": "get_company_info", "arguments": {"symbol": "AAPL"}}
    elif "exchange" in query_lower or "rate" in query_lower or "convert" in query_lower:
        return {"name": "get_exchange_rate", "arguments": {"from_currency": "USD", "to_currency": "EUR"}}
    else:
        # Default fallback
        return {"name": "get_stock_price", "arguments": {"symbol": "AAPL"}}

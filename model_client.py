import os
import requests
import json
from prompt import construct_prompt

def call_model_api(query: str) -> dict:
    """
    Calls the remote Model API and returns the tool call JSON.
    """
    model_api_url = os.getenv("MODEL_API_URL")
    if not model_api_url:
        raise ValueError("MODEL_API_URL environment variable is not set.")
        
    from tool_schemas import TOOLS
    payload = {
        "query": query,
        "tools": TOOLS
    }
    
    try:
        response = requests.post(model_api_url, json=payload, timeout=30)
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            # The server might have returned a 500 error or plain text
            return {"text_response": response.text}
        
        # If the API directly returns the tool call as a JSON object
        if "name" in data and "arguments" in data:
            return data
            
        # If it returns it wrapped in a 'response' or similar key
        for key in ["response", "tool_call", "message", "result"]:
            if key in data:
                model_response = data[key]
                # If it's a list of tool calls, take the first one
                if isinstance(model_response, list) and len(model_response) > 0:
                    model_response = model_response[0]
                    
                if isinstance(model_response, dict):
                    return model_response
                elif isinstance(model_response, str):
                    try:
                        return json.loads(model_response)
                    except json.JSONDecodeError:
                        # If it's a string but not valid JSON, treat it as a natural language response
                        return {"text_response": model_response}
        
        # If we reach here, check if data itself is a string
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {"text_response": data}
                
        return data
        
    except requests.exceptions.Timeout:
        raise RuntimeError("Model API request timed out.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to connect to Model API: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError("Model returned invalid JSON format.")

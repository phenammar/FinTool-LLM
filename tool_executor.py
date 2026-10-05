from tools import (
    get_stock_price,
    get_historical_prices,
    get_company_info,
    get_company_news,
    get_exchange_rate
)

# Registry mapping tool names to functions
TOOL_REGISTRY = {
    "get_stock_price": get_stock_price,
    "get_historical_prices": get_historical_prices,
    "get_company_info": get_company_info,
    "get_company_news": get_company_news,
    "get_exchange_rate": get_exchange_rate,
}

def execute_tool(name: str, arguments: dict) -> dict:
    """
    Executes a tool by name with the given arguments.
    """
    if name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool name: {name}")
        
    tool_func = TOOL_REGISTRY[name]
    
    try:
        # Unpack arguments and call the tool function
        result = tool_func(**arguments)
        return result
    except TypeError as e:
        raise ValueError(f"Invalid arguments for tool '{name}': {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error executing tool '{name}': {str(e)}")

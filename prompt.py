import json
from tool_schemas import TOOLS

def construct_prompt(query: str) -> str:
    """
    Constructs the prompt for the LLM to select a tool and provide its arguments.
    """
    system_prompt = (
        "You are a helpful assistant with access to tools. "
        "Your task is to select the most appropriate tool to answer the user's query and extract the required arguments. "
        "You MUST respond ONLY with a valid JSON object containing 'name' and 'arguments'. "
        "Do not include any other text, markdown formatting, or explanations.\n\n"
        "Available tools:\n"
        f"{json.dumps(TOOLS, indent=2)}\n\n"
        "Example Response:\n"
        "{\n"
        "  \"name\": \"get_stock_price\",\n"
        "  \"arguments\": {\n"
        "    \"symbol\": \"AAPL\"\n"
        "  }\n"
        "}\n"
    )
    
    prompt = f"{system_prompt}\nUser Query: {query}\n"
    return prompt

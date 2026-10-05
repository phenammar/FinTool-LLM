import json
from tool_schemas import TOOLS

def construct_prompt(query: str) -> str:
    prompt = f"""You are a tool-calling assistant.

    Tools:
        {json.dumps(TOOLS, indent=2)}

    Rules:
        1. You may ONLY use tools listed above.
        2. If none of the available tools can answer the query, do NOT call any tool.
        3. Do NOT invent tool names.
        4. Do NOT use a tool for an indirect or unrelated purpose.
        5. If no suitable tool exists, answer naturally that no suitable tool is available.
        6. Do not explain how to use a tool.
        7. For a valid tool call, return only the JSON tool call.

    Query:
        {query}

    Answer:
    """
    return prompt

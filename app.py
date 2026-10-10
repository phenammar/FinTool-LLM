import streamlit as st
from dotenv import load_dotenv
import json

from model_client import call_model_api
from tool_executor import execute_tool

# Load environment variables
load_dotenv()

st.set_page_config(page_title="FinTool", page_icon="🔧", layout="centered")

st.title("FinTool")
st.markdown("This application demonstrates local tool execution based on remote LLM tool selection.")

query = st.text_area("Query", placeholder="e.g. What is the current stock price of Apple?")

if st.button("Run"):
    if not query.strip():
        st.error("Please enter a query.")
    else:
        try:
            with st.spinner("Calling Model API..."):
                model_response = call_model_api(query)

            # Normalize single tool call into a list
            # This allows the app to handle both:
            # - one tool
            # - multiple tools
            if isinstance(model_response, dict):
                model_response = [model_response]

            elif not isinstance(model_response, list):
                st.error("Invalid response from Model API.")
                st.stop()

            # Handle natural language fallback
            if len(model_response) == 1 and "text_response" in model_response[0]:
                st.info("No suitable tool found.")
                st.stop()

            from tool_executor import TOOL_REGISTRY

            # Execute all selected tools
            for i, tool_call in enumerate(model_response, start=1):

                if not isinstance(tool_call, dict):
                    st.error(f"Invalid tool call at position {i}.")
                    continue

                tool_name = tool_call.get("name")
                tool_arguments = tool_call.get("arguments")

                if not tool_name:
                    st.error(f"Tool call {i} does not contain a tool name.")
                    continue

                if tool_name not in TOOL_REGISTRY:
                    st.error(f"Unknown tool: {tool_name}")
                    continue

                if tool_arguments is None:
                    st.error(f"Tool '{tool_name}' did not return 'arguments'.")
                    continue

                st.subheader(f"Tool {i}")
                st.code(tool_name, language="text")

                st.subheader("Arguments")
                st.json(tool_arguments)

                with st.spinner(f"Executing {tool_name}..."):
                    result = execute_tool(tool_name, tool_arguments)

                st.subheader("Tool Result")
                st.json(result)

        except ValueError as ve:
            st.error(f"Validation Error: {ve}")

        except RuntimeError as re:
            st.error(f"Runtime Error: {re}")

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

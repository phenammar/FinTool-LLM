import streamlit as st
from dotenv import load_dotenv
import json

from model_client import call_model_api
from tool_executor import execute_tool

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Tool Calling Demo", page_icon="🔧", layout="centered")

st.title("Tool Calling Demo")
st.markdown("This application demonstrates local tool execution based on remote LLM tool selection.")

query = st.text_area("Query", placeholder="e.g. What is the current stock price of Apple?")

if st.button("Run"):
    if not query.strip():
        st.error("Please enter a query.")
    else:
        try:
            with st.spinner("Calling Model API..."):
                model_response = call_model_api(query)
            
            # Validate model response
            if not isinstance(model_response, dict):
                st.error("Invalid response from Model API (expected JSON object).")
                st.stop()
                
            tool_name = model_response.get("name")
            tool_arguments = model_response.get("arguments")
            
            if not tool_name:
                st.error("Model did not return a tool 'name'.")
                st.stop()
                
            if tool_arguments is None:
                st.error("Model did not return 'arguments'.")
                st.stop()

            st.subheader("Tool Used")
            st.code(tool_name, language="text")
            
            st.subheader("Arguments")
            st.json(tool_arguments)
            
            with st.spinner("Executing Tool..."):
                result = execute_tool(tool_name, tool_arguments)
                
            st.subheader("Tool Result")
            st.json(result)
            
        except ValueError as ve:
            st.error(f"Validation Error: {ve}")
        except RuntimeError as re:
            st.error(f"Runtime Error: {re}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

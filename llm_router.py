"""
llm_router.py - OpenRouter API integration for AI completions
"""

import os
import requests
import streamlit as st

@st.cache_data
def call_openrouter(prompt, system_prompt="You are a helpful AI assistant."):
    """
    Call OpenRouter API to get AI completions
    
    Args:
        prompt (str): User prompt to send to the model
        system_prompt (str): System instructions for the model
        
    Returns:
        str: Model completion text
    """
    # Get API key from Streamlit secrets or environment variable
    api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))
    
    if not api_key:
        st.warning("OpenRouter API key not found. Please set it in .streamlit/secrets.toml or as an environment variable.")
        return "API key not configured. Please set OPENROUTER_API_KEY."
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  # Free & fast
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                headers=headers, 
                                json=data)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error calling OpenRouter API: {str(e)}")
        return f"Error: {str(e)}"

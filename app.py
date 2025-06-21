"""
AI Use Case Navigator - Main Application

A Streamlit application that displays a searchable and filterable table of AI use cases
across different companies and industries, with semantic search capabilities.
"""

import streamlit as st
import pandas as pd
import os

# Import our modules
from data_utils import load_data, filter_data, get_unique_values, prepare_display_dataframe
from ui import render_sidebar_filters, render_search_ui, render_cards, render_table, inject_custom_css
from search import semantic_search
from llm_router import call_openrouter

# Set page configuration
st.set_page_config(
    page_title="AI Use Case Navigator",
    page_icon="🤖",
    layout="wide"
)

# Inject custom CSS

inject_custom_css()

def main():
    st.title("AI Use Case Navigator")
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    selected_business_function, selected_ai_type, show_as_table = render_sidebar_filters(df)
    
    # Search UI
    text_search, semantic_search_query, use_semantic_search = render_search_ui()
    
    # Add OpenRouter AI assistant section in sidebar
    with st.sidebar:
        st.markdown("---")
        st.subheader("💬 AI Assistant")
        ai_prompt = st.text_area("Ask about AI use cases:", "", help="Ask questions about AI use cases or get recommendations")
        
        if st.button("Get AI Response"):
            if ai_prompt:
                with st.spinner("Generating response..."):
                    system_prompt = "You are an AI expert who helps users understand AI use cases. Provide concise, helpful responses about AI applications in business."
                    response = call_openrouter(ai_prompt, system_prompt)
                    st.info(response)
    
    # Handle semantic search
    if use_semantic_search and semantic_search_query:
        with st.spinner("Performing semantic search..."):
            # Get semantic search results
            search_results = semantic_search(semantic_search_query, df)
            
            # Display results
            st.subheader(f"Semantic Search Results for: '{semantic_search_query}'")
            
            # Extract similarity scores
            similarity_scores = search_results['similarity']
            
            # Display results count
            st.write(f"Found {len(search_results)} semantically similar use cases")
            
            # Render cards with similarity scores
            render_cards(search_results, similarity_scores)
            
            # Show as table if requested
            if show_as_table:
                display_df = prepare_display_dataframe(search_results)
                render_table(display_df)
    else:
        # Filter data based on selections
        filtered_df = filter_data(df, selected_business_function, selected_ai_type, text_search)
        
        # Display results count
        st.write(f"Displaying {len(filtered_df)} of {len(df)} use cases")
        
        # Render cards
        render_cards(filtered_df)
        
        # Show as table if requested
        if show_as_table:
            display_df = prepare_display_dataframe(filtered_df)
            render_table(display_df)

if __name__ == "__main__":
    main()

"""
data_utils.py - Utilities for loading and processing data for the AI Use Case Navigator
"""

import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data(file_path="Data/ai_use_case_navigator_cleaned_test.csv"):
    """
    Load data from CSV file with caching for improved performance
    """
    if not os.path.exists(file_path):
        st.error(f"Data file not found: {file_path}")
        return pd.DataFrame()
    
    return pd.read_csv(file_path)

@st.cache_data
def format_slug(slug):
    """
    Format slugs to readable text
    """
    if pd.isna(slug):
        return ""
    
    # Replace underscores with spaces
    formatted = slug.replace('_', ' ')
    # Replace slashes with spaces
    formatted = formatted.replace('/', ' ')
    # Replace parentheses
    formatted = formatted.replace('(', ' ').replace(')', ' ')
    # Capitalize each word
    formatted = ' '.join(word.capitalize() for word in formatted.split())
    return formatted

@st.cache_data
def filter_data(df, business_function="All", ai_type="All", search_term=""):
    """
    Filter dataframe based on selected filters and search term
    """
    filtered_df = df.copy()
    
    # Apply Business Function filter
    if business_function != "All":
        filtered_df = filtered_df[filtered_df["business_function"] == business_function]
    
    # Apply AI Type filter
    if ai_type != "All":
        filtered_df = filtered_df[filtered_df["ai_type"] == ai_type]
    
    # Apply text search filter (if not using semantic search)
    if search_term:
        search_mask = (
            filtered_df["company"].str.contains(search_term, case=False, na=False) | 
            filtered_df["use_case_name"].str.contains(search_term, case=False, na=False) |
            filtered_df["outcome"].str.contains(search_term, case=False, na=False) |
            filtered_df["business_function"].str.contains(search_term, case=False, na=False) |
            filtered_df["ai_type"].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[search_mask]
    
    return filtered_df

@st.cache_data
def get_unique_values(df):
    """
    Get unique values for filters
    """
    business_functions = ["All"] + sorted(df["business_function"].unique().tolist())
    ai_types = ["All"] + sorted(df["ai_type"].unique().tolist())
    
    return business_functions, ai_types

def prepare_display_dataframe(filtered_df):
    """
    Prepare a dataframe for display in the table view
    """
    display_df = filtered_df.copy()
    
    # Convert source_link to markdown links for compatibility
    if 'source_link' in display_df.columns:
        display_df['source_link'] = display_df.apply(
            lambda row: f"[Link]({row['source_link']})" if pd.notna(row['source_link']) else "", 
            axis=1
        )
    
    # Format slugs if they exist
    if 'ai_type_slug' in display_df.columns:
        display_df['ai_type_slug'] = display_df['ai_type_slug'].apply(format_slug)
        
    if 'business_function_slug' in display_df.columns:
        display_df['business_function_slug'] = display_df['business_function_slug'].apply(format_slug)
    
    return display_df

"""
data_utils.py - Utilities for loading and processing data for the AI Use Case Navigator
"""

import pandas as pd
import streamlit as st
import os
import re
from typing import Dict, Optional

def clean_column_names(df):
    """
    Standardize column names by:
    - Converting to lowercase
    - Replacing spaces with underscores
    - Removing special characters
    - Ensuring consistent naming conventions
    """
    # Create a mapping of common variations to standardized names
    column_name_mapping = {
        'ai type': 'ai_type',
        'ai_type': 'ai_type',
        'aitype': 'ai_type',
        'ai-type': 'ai_type',
        'type of ai': 'ai_type',
        'ai technology': 'ai_type',
        
        'business function': 'business_function',
        'business_function': 'business_function',
        'businessfunction': 'business_function',
        'business-function': 'business_function',
        'function': 'business_function',
        'department': 'business_function',
        
        'company': 'company',
        'organization': 'company',
        'company name': 'company',
        'org': 'company',
        
        'use case': 'use_case_name',
        'use_case': 'use_case_name',
        'use case name': 'use_case_name',
        'use_case_name': 'use_case_name',
        'usecase': 'use_case_name',
        'case name': 'use_case_name',
        'project': 'use_case_name',
        
        'outcome': 'outcome',
        'result': 'outcome',
        'impact': 'outcome',
        'benefits': 'outcome',
        'results': 'outcome',
        
        'source': 'source_link',
        'link': 'source_link',
        'url': 'source_link',
        'source_link': 'source_link',
        'reference': 'source_link',
        
        'ai_type_slug': 'ai_type_slug',
        'aitype_slug': 'ai_type_slug',
        'ai_slug': 'ai_type_slug',
        
        'business_function_slug': 'business_function_slug',
        'function_slug': 'business_function_slug',
        'business_slug': 'business_function_slug'
    }
    
    # Create a new list of standardized column names
    new_columns = []
    for col in df.columns:
        # Convert to lowercase and strip whitespace
        clean_col = col.lower().strip()
        
        # Check if the column name is in our mapping
        if clean_col in column_name_mapping:
            new_columns.append(column_name_mapping[clean_col])
        else:
            # If not in mapping, apply standard cleaning
            # Replace spaces with underscores
            clean_col = re.sub(r'\s+', '_', clean_col)
            # Remove special characters except underscores
            clean_col = re.sub(r'[^\w_]', '', clean_col)
            new_columns.append(clean_col)
    
    # Rename the columns
    df.columns = new_columns
    
    return df

@st.cache_data(ttl=60)
def load_data(file_path="Data/ai_use_case_navigator_merged.csv", remove_duplicates=False):
    """
    Load data from CSV file with caching for improved performance
    Also performs comprehensive data cleaning operations from datacleaner.py
    
    Args:
        file_path (str): Path to the CSV file to load
        remove_duplicates (bool): Whether to remove duplicate entries
    """
    if not os.path.exists(file_path):
        st.error(f"Data file not found: {file_path}")
        return pd.DataFrame()
    
    try:
        # Read the CSV file with robust error handling
        df = pd.read_csv(file_path, engine='python', on_bad_lines='skip', quotechar='"', escapechar='\\')
        
        # Store original row and column count for logging
        original_rows = len(df)
        original_cols = len(df.columns)
        print(f"Original columns: {df.columns.tolist()}")
        
        # First, standardize all column names to lowercase
        df.columns = [col.lower() for col in df.columns]
        
        # Identify and handle duplicate columns
        seen_columns = {}
        duplicate_cols = []
        
        for i, col in enumerate(df.columns):
            if col in seen_columns:
                duplicate_cols.append(i)
            else:
                seen_columns[col] = i
        
        # Drop duplicate columns
        if duplicate_cols:
            print(f"Found {len(duplicate_cols)} duplicate columns. Removing duplicates...")
            df = df.drop(df.columns[duplicate_cols], axis=1)
            print(f"Columns after removing duplicates: {df.columns.tolist()}")
        
        # Now apply more specific column name standardization
        # Create a mapping of common variations to standardized names
        column_name_mapping = {
            'company': 'company',
            'organization': 'company',
            'company name': 'company',
            'org': 'company',
            
            'use case': 'use_case_name',
            'use_case': 'use_case_name',
            'use case name': 'use_case_name',
            'usecase': 'use_case_name',
            'case name': 'use_case_name',
            'project': 'use_case_name',
            
            'business function': 'business_function',
            'businessfunction': 'business_function',
            'business-function': 'business_function',
            'function': 'business_function',
            'department': 'business_function',
            
            'ai type': 'ai_type',
            'aitype': 'ai_type',
            'ai-type': 'ai_type',
            'type of ai': 'ai_type',
            'ai technology': 'ai_type',
            
            'outcome': 'outcome',
            'result': 'outcome',
            'impact': 'outcome',
            'benefits': 'outcome',
            'results': 'outcome',
            
            'source': 'source_link',
            'link': 'source_link',
            'url': 'source_link',
            'reference': 'source_link',
        }
        
        # Rename columns based on mapping
        rename_dict = {}
        for col in df.columns:
            if col in column_name_mapping:
                rename_dict[col] = column_name_mapping[col]
        
        if rename_dict:
            df = df.rename(columns=rename_dict)
            print(f"Columns after standardization: {df.columns.tolist()}")
        
        # Ensure required columns exist
        required_columns = ['company', 'use_case_name', 'business_function', 'ai_type', 'outcome', 'source_link']
        for col in required_columns:
            if col not in df.columns:
                print(f"Adding missing column: {col}")
                df[col] = ""
        
        # Remove duplicates only if requested
        if remove_duplicates and 'company' in df.columns and 'use_case_name' in df.columns:
            initial_count = len(df)
            df = df.drop_duplicates(subset=['company', 'use_case_name'])
            duplicates_removed = initial_count - len(df)
            if duplicates_removed > 0:
                print(f"Removed {duplicates_removed} duplicate entries.")
        else:
            # If not removing duplicates, just log the count of potential duplicates
            if 'company' in df.columns and 'use_case_name' in df.columns:
                potential_duplicates = len(df) - len(df.drop_duplicates(subset=['company', 'use_case_name']))
                if potential_duplicates > 0:
                    print(f"Note: Dataset contains {potential_duplicates} potential duplicate entries (not removed).")
            else:
                print("Cannot check for duplicates: required columns missing.")

        
        # Generate slugs if needed
        if 'ai_type' in df.columns and 'ai_type_slug' not in df.columns:
            df['ai_type_slug'] = df['ai_type'].apply(lambda x: slugify(str(x)) if not pd.isna(x) else "")
            
        if 'business_function' in df.columns and 'business_function_slug' not in df.columns:
            df['business_function_slug'] = df['business_function'].apply(lambda x: slugify(str(x)) if not pd.isna(x) else "")
        
        return df
    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def slugify(text):
    """
    Convert text to slug format (lowercase, replace spaces and slashes with underscores)
    """
    if pd.isna(text):
        return ""
    
    # Convert to lowercase
    slug = text.lower()
    # Replace slashes with underscores
    slug = slug.replace('/', '_')
    # Replace spaces with underscores
    slug = slug.replace(' ', '_')
    # Remove special characters
    slug = re.sub(r'[^\w_]', '', slug)
    
    return slug

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
    Get unique values for filters from the dataframe
    
    Args:
        df (pd.DataFrame): DataFrame containing business_function and ai_type columns
        
    Returns:
        tuple: (business_functions, ai_types) lists including 'All' option
    """
    business_functions = ["All"] + sorted(df["business_function"].unique().tolist())
    ai_types = ["All"] + sorted(df["ai_type"].unique().tolist())
    
    return business_functions, ai_types

# Dictionary mapping company names to their domains
# Only includes companies that commonly need special handling
COMPANY_DOMAINS: Dict[str, str] = {
    "Amazon": "amazon.com",
    "Netflix": "netflix.com",
    "Google": "google.com",
    "Microsoft": "microsoft.com",
    "IBM": "ibm.com",
    "JPMorgan Chase": "jpmorganchase.com",
    "American Express": "americanexpress.com",
    "Coca-Cola": "coca-cola.com"
    # Other companies will use the automatic domain generation
}

def get_domain_from_company(company_name: str) -> str:
    """
    Get the domain for a company name.
    Uses predefined mapping or derives from company name.
    
    Args:
        company_name (str): Name of the company
        
    Returns:
        str: Domain name for the company
    """
    # Check if we have a predefined domain
    if company_name in COMPANY_DOMAINS:
        return COMPANY_DOMAINS[company_name]
    
    # Otherwise, try to derive domain from company name
    # Remove special characters, spaces, and convert to lowercase
    domain = re.sub(r'[^\w\s]', '', company_name)
    domain = domain.lower().replace(' ', '')
    
    # Add .com as default TLD
    if not domain.endswith('.com'):
        domain = f"{domain}.com"
    
    return domain

def generate_logo_url(domain: str, token: Optional[str] = None) -> str:
    """
    Generate a logo URL using img.logo.dev API.
    
    Args:
        domain (str): Domain name to generate logo for
        token (Optional[str]): API token for img.logo.dev
        
    Returns:
        str: URL to the company logo
    """
    if token and token != "YOUR_TOKEN":
        return f"https://img.logo.dev/{domain}?token={token}"
    return f"https://img.logo.dev/{domain}"

@st.cache_data
def generate_logo_url_column(df, token=None):
    """
    Generate a company_logo column with Logo.dev image URLs using the company name
    
    """
    # Check if 'company' column exists
    if 'company' not in df.columns:
        print("WARNING: 'company' column not found in dataframe. Cannot generate logo URLs.")
        # Create an empty logo column
        df['company_logo'] = ""
        return df
    
    try:
        # Generate logo URLs
        df['company_logo'] = df['company'].apply(
            lambda company: generate_logo_url(get_domain_from_company(company), token=token)
        )
    except Exception as e:
        print(f"ERROR generating logo URLs: {str(e)}")
        # Create a fallback logo column
        df['company_logo'] = ""
    
    return df

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

# End of file

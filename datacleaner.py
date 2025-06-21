#!/usr/bin/env python3
"""
datacleaner.py - A script to clean CSV data for the AI Use Case Navigator

This script performs the following operations:
1. Loads a CSV file
2. Removes duplicate entries
3. Standardizes column names
4. Ensures consistent formatting
5. Saves the cleaned data to a new CSV file
"""

import pandas as pd
import os
import re
import argparse
from datetime import datetime

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

def generate_slugs(df):
    """
    Generate slugs for ai_type and business_function if they don't exist
    """
    # Check if the dataframe has the required columns
    if 'ai_type' in df.columns and 'ai_type_slug' not in df.columns:
        df['ai_type_slug'] = df['ai_type'].apply(create_slug)
    
    if 'business_function' in df.columns and 'business_function_slug' not in df.columns:
        df['business_function_slug'] = df['business_function'].apply(create_slug)
    
    return df

def create_slug(text):
    """
    Create a slug from text:
    - Convert to lowercase
    - Replace spaces with underscores
    - Remove special characters
    """
    if pd.isna(text):
        return ""
    
    # Convert to lowercase
    slug = text.lower()
    # Replace spaces, slashes, and parentheses with underscores
    slug = re.sub(r'[\s/()]', '_', slug)
    # Remove any other special characters
    slug = re.sub(r'[^\w_]', '', slug)
    # Replace multiple underscores with a single one
    slug = re.sub(r'_+', '_', slug)
    # Remove leading and trailing underscores
    slug = slug.strip('_')
    
    return slug

def remove_duplicates(df):
    """
    Remove duplicate entries based on company and use_case_name
    """
    # Check if the dataframe has the required columns
    if 'company' in df.columns and 'use_case_name' in df.columns:
        # Count initial rows
        initial_count = len(df)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['company', 'use_case_name'])
        
        # Count final rows
        final_count = len(df)
        
        # Report how many duplicates were removed
        duplicates_removed = initial_count - final_count
        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate entries.")
    
    return df

def ensure_required_columns(df):
    """
    Ensure that the dataframe has all required columns
    """
    required_columns = [
        'company', 
        'use_case_name', 
        'business_function', 
        'ai_type', 
        'outcome', 
        'source_link'
    ]
    
    for col in required_columns:
        if col not in df.columns:
            # Create empty column if it doesn't exist
            df[col] = ""
            print(f"Added missing column: {col}")
    
    return df

def clean_data(input_file, output_file=None):
    """
    Main function to clean the CSV data
    """
    print(f"Loading data from {input_file}...")
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return False
    
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # Store original row and column count
        original_rows = len(df)
        original_cols = len(df.columns)
        
        print(f"Original data: {original_rows} rows, {original_cols} columns")
        print(f"Original columns: {', '.join(df.columns)}")
        
        # Clean column names
        df = clean_column_names(df)
        
        # Ensure required columns exist
        df = ensure_required_columns(df)
        
        # Remove duplicates
        df = remove_duplicates(df)
        
        # Generate slugs if needed
        df = generate_slugs(df)
        
        # If no output file specified, create one based on the input file
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{base_name}_cleaned_{timestamp}.csv"
        
        # Save the cleaned data
        df.to_csv(output_file, index=False)
        
        # Report results
        print(f"Cleaned data saved to {output_file}")
        print(f"Final data: {len(df)} rows, {len(df.columns)} columns")
        print(f"Final columns: {', '.join(df.columns)}")
        
        return True
    
    except Exception as e:
        print(f"Error cleaning data: {str(e)}")
        return False

def main():
    """
    Parse command line arguments and run the data cleaning process
    """
    parser = argparse.ArgumentParser(description="Clean CSV data for AI Use Case Navigator")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("-o", "--output", help="Path to the output CSV file (optional)")
    
    args = parser.parse_args()
    
    clean_data(args.input_file, args.output)

if __name__ == "__main__":
    main()

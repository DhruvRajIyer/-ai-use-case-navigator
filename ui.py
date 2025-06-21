"""
ui.py - UI components for the AI Use Case Navigator
"""

import streamlit as st
import pandas as pd

def create_tag(text, tag_type):
    """
    Create a styled tag for AI Type or Business Function
    """
    if tag_type == "ai_type":
        class_name = "ai-type-tag"
    else:
        class_name = "business-function-tag"
    return f"<div class='tag-container {class_name}'>{text}</div>"

def render_sidebar_filters(df):
    """
    Render sidebar filters for Business Function and AI Type
    """
    st.sidebar.header("Filters")
    
    # Business Function filter - with error handling
    try:
        if 'business_function' in df.columns:
            # Get unique values, handling potential NaN values
            bf_values = df['business_function'].dropna().unique()
            business_functions = ["All"] + sorted([str(bf) for bf in bf_values])
        else:
            st.sidebar.warning("Business Function data not available")
            business_functions = ["All"]
    except Exception as e:
        st.sidebar.error(f"Error loading business functions: {str(e)}")
        business_functions = ["All"]
        
    selected_business_function = st.sidebar.selectbox(
        "Business Function",
        business_functions
    )
    
    # AI Type filter - with error handling
    try:
        if 'ai_type' in df.columns:
            # Get unique values, handling potential NaN values
            ai_values = df['ai_type'].dropna().unique()
            ai_types = ["All"] + sorted([str(ai) for ai in ai_values])
        else:
            st.sidebar.warning("AI Type data not available")
            ai_types = ["All"]
    except Exception as e:
        st.sidebar.error(f"Error loading AI types: {str(e)}")
        ai_types = ["All"]
        
    selected_ai_type = st.sidebar.selectbox(
        "AI Type",
        ai_types
    )
    
    # View options
    show_as_table = st.sidebar.checkbox("Show as table")
    
    return selected_business_function, selected_ai_type, show_as_table

def render_search_ui():
    """
    Render search UI components
    """
    st.sidebar.header("Search")
    
    # Text search
    text_search = st.sidebar.text_input("Keyword Search", "")
    
    # Semantic search
    st.sidebar.markdown("---")
    st.sidebar.subheader("Semantic Search")
    semantic_search_query = st.sidebar.text_area("Find similar use cases", "", 
                                               help="Enter a description to find semantically similar use cases")
    use_semantic_search = st.sidebar.button("Search")
    
    return text_search, semantic_search_query, use_semantic_search

def render_card(row, col, similarity_score=None):
    """
    Render a single use case card
    """
    with col:
        with st.container():
            # Add custom border styling
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            # Display company logo with fallback to NA.jpg
            logo_url = row.get('company_logo', '')
            if pd.isna(logo_url) or not logo_url:
                logo_url = 'assets/NA.jpg'
                
            st.markdown(
                f"<div style='text-align: center;'><img src='{logo_url}' width='100' onerror=\"this.onerror=null; this.src='assets/NA.jpg';\"></div>",
                unsafe_allow_html=True
            )
            
            # Card header
            st.markdown(f"### {row['use_case_name']}")
            st.markdown(f"**Company:** {row['company']}")
            
            # Display similarity score if available
            if similarity_score is not None:
                st.markdown(f"**Similarity:** {similarity_score:.2f}")
            
            # Styled tags
            ai_type_tag = create_tag(row['ai_type'], "ai_type")
            business_function_tag = create_tag(row['business_function'], "business_function")
            st.markdown(f"{ai_type_tag} {business_function_tag}", unsafe_allow_html=True)
            
            # Expandable details
            with st.expander("View Details"):
                st.markdown("### Outcome")
                st.write(row['outcome'])
                
                st.markdown("### Source")
                if pd.notna(row['source_link']):
                    st.markdown(f"[View Source]({row['source_link']})")
                else:
                    st.write("No source link available")
                
                # Additional metadata if available
                if 'ai_type_slug' in row and 'business_function_slug' in row:
                    st.markdown("### Metadata")
                    from data_utils import format_slug
                    formatted_ai_type = format_slug(row['ai_type_slug'])
                    formatted_business_function = format_slug(row['business_function_slug'])
                    st.write(f"AI Type: {formatted_ai_type}")
                    st.write(f"Business Function: {formatted_business_function}")
            
            # Close the custom card div
            st.markdown("</div>", unsafe_allow_html=True)

def render_cards(filtered_df, similarity_scores=None):
    """
    Render use case cards in a two-column layout
    """
    if not filtered_df.empty:
        # Create two columns for the cards
        col1, col2 = st.columns(2)
        
        # Distribute cards between the two columns
        for i, (idx, row) in enumerate(filtered_df.iterrows()):
            # Alternate between columns
            current_col = col1 if i % 2 == 0 else col2
            
            # Get similarity score if available
            similarity = None
            if similarity_scores is not None and idx in similarity_scores.index:
                similarity = similarity_scores.loc[idx]
            
            # Render card
            render_card(row, current_col, similarity)
    else:
        st.warning("No use cases match your filters. Please try different criteria.")

def render_table(display_df):
    """
    Render a table view of the data
    """
    st.subheader("Table View")
    st.dataframe(
        display_df,
        column_config={
            "company": "Company",
            "use_case_name": "Use Case",
            "business_function": "Business Function",
            "ai_type": "AI Type",
            "outcome": "Outcome",
            "source_link": "Source",
            "ai_type_slug": "AI Type (Formatted)",
            "business_function_slug": "Business Function (Formatted)",
            "similarity": "Similarity"
        },
        hide_index=True,
        use_container_width=True
    )

def inject_custom_css():
    """
    Inject custom CSS for styling
    """
    st.markdown("""
    <style>
        .tag-container {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
            margin-right: 5px;
            margin-bottom: 5px;
            color: white;
        }
        .ai-type-tag {
            background-color: #3366ff;
        }
        .business-function-tag {
            background-color: #ff6633;
        }
        .card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .card-header {
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        .company-name {
            color: #666;
            font-size: 0.9em;
        }
        .card-content {
            margin-top: 10px;
        }
        .similarity-score {
            color: #3366ff;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

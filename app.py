import streamlit as st
import pandas as pd
import random

# Set page configuration
st.set_page_config(
    page_title="AI Use Case Navigator",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for styling
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
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Data/ai_use_case_navigator_cleaned.csv")

# Generate consistent colors for tags
@st.cache_data
def get_tag_colors(items, base_hue=0):
    colors = {}
    for i, item in enumerate(items):
        hue = (base_hue + i * 25) % 360
        colors[item] = f"hsl({hue}, 70%, 50%)"
    return colors

# Format slugs to readable text
def format_slug(slug):
    # Replace underscores with spaces
    formatted = slug.replace('_', ' ')
    # Replace slashes with spaces
    formatted = formatted.replace('/', ' ')
    # Replace parentheses
    formatted = formatted.replace('(', ' ').replace(')', ' ')
    # Capitalize each word
    formatted = ' '.join(word.capitalize() for word in formatted.split())
    return formatted

# Create a styled tag
def create_tag(text, tag_type):
    if tag_type == "ai_type":
        class_name = "ai-type-tag"
    else:
        class_name = "business-function-tag"
    return f"<div class='tag-container {class_name}'>{text}</div>"

# Main function
def main():
    st.title("AI Use Case Navigator")
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Business Function filter
    business_functions = ["All"] + sorted(df["business_function"].unique().tolist())
    selected_business_function = st.sidebar.selectbox(
        "Business Function",
        business_functions
    )
    
    # AI Type filter
    ai_types = ["All"] + sorted(df["ai_type"].unique().tolist())
    selected_ai_type = st.sidebar.selectbox(
        "AI Type",
        ai_types
    )
    
    # Enhanced keyword search
    st.sidebar.subheader("Keyword Search")
    search_term = st.sidebar.text_input("Search in all fields")
    
    # Apply filters
    filtered_df = df.copy()
    
    # Apply Business Function filter
    if selected_business_function != "All":
        filtered_df = filtered_df[filtered_df["business_function"] == selected_business_function]
    
    # Apply AI Type filter
    if selected_ai_type != "All":
        filtered_df = filtered_df[filtered_df["ai_type"] == selected_ai_type]
    
    # Apply enhanced search filter
    if search_term:
        search_mask = (
            filtered_df["company"].str.contains(search_term, case=False) | 
            filtered_df["use_case_name"].str.contains(search_term, case=False) |
            filtered_df["outcome"].str.contains(search_term, case=False) |
            filtered_df["business_function"].str.contains(search_term, case=False) |
            filtered_df["ai_type"].str.contains(search_term, case=False)
        )
        filtered_df = filtered_df[search_mask]
    
    # Display results count
    st.write(f"Displaying {len(filtered_df)} of {len(df)} use cases")
    
    # Two-column card layout
    if not filtered_df.empty:
        # Create two columns for the cards
        col1, col2 = st.columns(2)
        
        # Distribute cards between the two columns
        for i, (_, row) in enumerate(filtered_df.iterrows()):
            # Alternate between columns
            current_col = col1 if i % 2 == 0 else col2
            
            # Create card with expandable view
            with current_col:
                with st.container():
                    # Add custom border styling
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    # Card header
                    st.markdown(f"### {row['use_case_name']}")
                    st.markdown(f"**Company:** {row['company']}")
                    
                    # Styled tags
                    ai_type_tag = create_tag(row['ai_type'], "ai_type")
                    business_function_tag = create_tag(row['business_function'], "business_function")
                    st.markdown(f"{ai_type_tag} {business_function_tag}", unsafe_allow_html=True)
                    
                    # Expandable details
                    with st.expander("View Details"):
                        st.markdown("### Outcome")
                        st.write(row['outcome'])
                        
                        st.markdown("### Source")
                        st.markdown(f"[View Source]({row['source_link']})")
                        
                        # Additional metadata if available
                        if 'ai_type_slug' in row and 'business_function_slug' in row:
                            st.markdown("### Metadata")
                            formatted_ai_type = format_slug(row['ai_type_slug'])
                            formatted_business_function = format_slug(row['business_function_slug'])
                            st.write(f"AI Type: {formatted_ai_type}")
                            st.write(f"Business Function: {formatted_business_function}")
                    
                    # Close the custom card div
                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No use cases match your filters. Please try different criteria.")

    # Option to view as traditional table
    if st.sidebar.checkbox("Show as table"):
        st.subheader("Table View")
        
        # Create a modified dataframe for display
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
        
        # Display the table
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
                "business_function_slug": "Business Function (Formatted)"
            },
            hide_index=True,
            use_container_width=True
        )

if __name__ == "__main__":
    main()

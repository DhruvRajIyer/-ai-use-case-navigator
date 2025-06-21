"""
search.py - Semantic search functionality using SentenceTransformer embeddings and FAISS
"""

import os
import numpy as np
import pandas as pd
import streamlit as st
import faiss
import pickle
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Constants
MODEL_NAME = "all-MiniLM-L6-v2"
FAISS_INDEX_PATH = "Data/faiss_index.pkl"
EMBEDDING_CACHE_PATH = "Data/embedding_cache.pkl"

# Load the model once at module level for reuse
@st.cache_resource
def get_model():
    return SentenceTransformer(MODEL_NAME)

@st.cache_data
def embed_texts(texts):
    """
    Generate embeddings for a list of texts using SentenceTransformer
    """
    model = get_model()
    return model.encode(texts, show_progress_bar=True)

def generate_embeddings(df):
    """
    Generate embeddings for all use cases in the dataframe
    """
    # Check if embeddings cache exists
    if os.path.exists(EMBEDDING_CACHE_PATH):
        try:
            with open(EMBEDDING_CACHE_PATH, 'rb') as f:
                cache_data = pickle.load(f)
                
            # If cache matches current data, use it
            if len(cache_data) == len(df) and all(cache_data['use_case_name'] == df['use_case_name']):
                st.success("Using cached embeddings")
                return cache_data['embedding'].tolist()
        except Exception as e:
            st.warning(f"Could not load embedding cache: {str(e)}")
    
    # Generate combined text for each use case (title + outcome)
    texts = []
    for _, row in df.iterrows():
        title = row['use_case_name'] if not pd.isna(row['use_case_name']) else ""
        company = row['company'] if not pd.isna(row['company']) else ""
        outcome = row['outcome'] if not pd.isna(row['outcome']) else ""
        ai_type = row['ai_type'] if not pd.isna(row['ai_type']) else ""
        business_function = row['business_function'] if not pd.isna(row['business_function']) else ""
        
        text = f"{title}. {company} used {ai_type} for {business_function}. {outcome}"
        texts.append(text)
    
    # Show progress message
    with st.spinner("Generating embeddings... (this may take a minute)"):
        # Generate embeddings for all texts at once
        embeddings = embed_texts(texts)
    
    # Cache the embeddings
    cache_df = df.copy()
    cache_df['embedding'] = embeddings.tolist()
    
    try:
        with open(EMBEDDING_CACHE_PATH, 'wb') as f:
            pickle.dump(cache_df, f)
    except Exception as e:
        st.warning(f"Could not save embedding cache: {str(e)}")
    
    return embeddings

@st.cache_data
def build_faiss_index(df):
    """
    Build a FAISS index from the dataframe
    """
    # Check if index exists
    if os.path.exists(FAISS_INDEX_PATH):
        try:
            with open(FAISS_INDEX_PATH, 'rb') as f:
                index_data = pickle.load(f)
                
            # If index matches current data, use it
            if len(index_data['ids']) == len(df):
                st.success("Using cached FAISS index")
                return index_data['index'], index_data['ids']
        except Exception as e:
            st.warning(f"Could not load FAISS index: {str(e)}")
    
    # Generate embeddings
    embeddings = generate_embeddings(df)
    
    # Convert to numpy array if not already
    if not isinstance(embeddings, np.ndarray):
        embeddings_np = np.array(embeddings).astype('float32')
    else:
        embeddings_np = embeddings.astype('float32')
    
    # Create FAISS index
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)
    
    # Create mapping from FAISS ids to dataframe indices
    ids = list(range(len(df)))
    
    # Save index
    try:
        with open(FAISS_INDEX_PATH, 'wb') as f:
            pickle.dump({'index': index, 'ids': ids}, f)
    except Exception as e:
        st.warning(f"Could not save FAISS index: {str(e)}")
    
    return index, ids

def rebuild_faiss_index(csv_path=None):
    """
    Force rebuild the FAISS index and embedding cache from scratch
    
    Args:
        csv_path: Path to the CSV file. If None, uses the default path.
    """
    # Remove existing index and cache files
    if os.path.exists(FAISS_INDEX_PATH):
        print(f"Removing existing index: {FAISS_INDEX_PATH}")
        os.remove(FAISS_INDEX_PATH)
    
    if os.path.exists(EMBEDDING_CACHE_PATH):
        print(f"Removing existing embedding cache: {EMBEDDING_CACHE_PATH}")
        os.remove(EMBEDDING_CACHE_PATH)
    
    # Load data
    if csv_path is None:
        csv_path = "Data/ai_use_case_navigator_cleaned_test.csv"
    
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Build index
    print("Building FAISS index...")
    index, ids = build_faiss_index(df)
    
    print(f"Index rebuilt successfully with {len(df)} items!")
    print(f"Index dimension: {index.d}")
    
    return index, ids, df

def semantic_search(query, df, top_k=5):
    """
    Search for similar use cases using semantic search
    """
    # Build FAISS index
    index, ids = build_faiss_index(df)
    
    # Get query embedding
    model = get_model()
    query_embedding = model.encode([query])[0]
    
    # Ensure correct dimensions
    dimension = index.d  # Get dimension from the index
    if len(query_embedding) != dimension:
        st.warning(f"Dimension mismatch: query embedding has {len(query_embedding)} dimensions, but index expects {dimension}")
        # Force rebuild the index
        if os.path.exists(FAISS_INDEX_PATH):
            os.remove(FAISS_INDEX_PATH)
        if os.path.exists(EMBEDDING_CACHE_PATH):
            os.remove(EMBEDDING_CACHE_PATH)
        # Rebuild index
        index, ids = build_faiss_index(df)
        # Re-encode query
        query_embedding = model.encode([query])[0]
    
    query_embedding_np = np.array([query_embedding]).astype('float32')
    
    # Search
    distances, indices = index.search(query_embedding_np, top_k)
    
    # Map FAISS indices to dataframe indices
    df_indices = [ids[i] for i in indices[0]]
    
    # Get results
    results = df.iloc[df_indices].copy()
    
    # Add distance scores (convert to similarity score)
    max_distance = np.max(distances)
    if max_distance > 0:
        results['similarity'] = 1 - (distances[0] / max_distance)
    else:
        results['similarity'] = np.ones(len(distances[0]))
    
    return results

# CLI functionality
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Use Case Navigator - FAISS Index Management")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the FAISS index from scratch")
    parser.add_argument("--csv", type=str, help="Path to CSV file (optional)")
    args = parser.parse_args()
    
    if args.rebuild:
        rebuild_faiss_index(args.csv)

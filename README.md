## 🚀 AI Use Case Navigator

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b.svg)](https://streamlit.io/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/ai-use-case-navigator/pulls)
[![Last Commit](https://img.shields.io/github/last-commit/yourusername/ai-use-case-navigator)](https://github.com/yourusername/ai-use-case-navigator/commits)

A **Streamlit** application that showcases real-world **AI use cases** across various industries and companies. Ideal for researchers, students, business leaders, and tech enthusiasts seeking inspiration or benchmarking examples.

---

## 🌟 Features

- 🔍 **Keyword Search** by company, use case name, or description  
- 🔮 **Semantic Search** using SentenceTransformer embeddings to find similar use cases
- 💬 **AI Assistant** powered by OpenRouter for answering questions about AI use cases
- 🧠 **Filter** by Business Function and AI Type  
- 📊 **Interactive table** with source links for each entry  
- 🎨 **Card Layout** with expandable details and colored tags
- 📁 **Cached Data Loading** for improved performance
- 💡 **Highlights** use case outcomes and AI adoption trends

---

## 🛠️ Setup & Usage

You can set up and run the application in multiple ways:

### ✅ Option 1: One-Click Setup Script

```bash
chmod +x setup.sh
./setup.sh
Creates a virtual environment, installs dependencies, and runs the app.
```

### ✅ Option 2: Using Makefile
```bash
Copy
Edit
make setup     # Set up the environment and install dependencies
make run       # Launch the application
Other available commands:

make install – Install dependencies

make clean – Remove .venv and cached files

make help – Display help message
```
### ✅ Option 3: Manual Virtual Environment Setup
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py    
```
### ✅ Option 4: Direct Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 📊 Data Structure
The application reads from:

```bash
Data/ai_use_case_navigator_cleaned.csv
```

### Columns:
```bash
Column-Name                Description

company                   Organization using AI
use_case_name             Title of the AI use case
business_function         Related business domain (e.g., HR, Finance)
ai_type                   Type of AI used (e.g., NLP, CV)
outcome                   Key result or benefit
source_link               Link to the original article or report
ai_type_slug              Slugified AI type (for filtering)
business_function_slug    Slugified business function (for filtering)
```

### 🧩 Application Structure

The application is modularized into several components:

- `app.py` - Main application entry point
- `data_utils.py` - Data loading and processing utilities
- `search.py` - Semantic search functionality using SentenceTransformer embeddings and FAISS
- `ui.py` - UI components and rendering functions
- `llm_router.py` - OpenRouter API integration for AI assistant
- `.streamlit/config.toml` - Custom theme configuration
- `.streamlit/secrets.toml` - API keys and secrets storage

### 🧹 Data Cleaning
The repository includes a data cleaning script to standardize CSV files:

```bash
python3 datacleaner.py input_file.csv -o output_file.csv
```

The script performs the following operations:
- Standardizes column names (e.g., "AI type" → "ai_type")
- Removes duplicate entries
- Generates slugs for AI types and business functions
- Ensures all required columns exist

Options:
- `input_file.csv`: Path to the input CSV file (required)
- `-o, --output`: Path to the output CSV file (optional, generates timestamped file if not specified)

### 🔄 Rebuilding the Search Index
If you encounter dimension mismatch errors or want to force rebuild the FAISS index:

```bash
# Simply delete these files and restart the app
rm Data/faiss_index.pkl Data/embedding_cache.pkl

# Then restart the Streamlit app
streamlit run app.py
```

The app will automatically:
- Detect that the index files are missing
- Regenerate embeddings using the SentenceTransformer model
- Create a new FAISS index for semantic search

### 📎 Requirements
Python 3.12+

- Streamlit
- Pandas
- SentenceTransformer (for embeddings generation)
- FAISS (for similarity search)
- Requests (for OpenRouter API calls)
- NumPy, SciPy, tqdm (for data processing)

(Install everything using requirements.txt)

### 🔑 API Keys Setup

#### OpenRouter API (for AI Assistant)
To use the AI assistant feature, you need to set up an OpenRouter API key:

1. Sign up at [OpenRouter](https://openrouter.ai/) and get your API key
2. Add your key to `.streamlit/secrets.toml`:

```toml
OPENROUTER_API_KEY = "your-api-key-here"
```

#### Logo.dev API (for Company Logos)
To display company logos in the UI, you need a Logo.dev API token:

1. Sign up at [Logo.dev](https://logo.dev/) and get your API token
2. Add your token to `.streamlit/secrets.toml`:

```toml
LOGO_DEV_TOKEN = "your-token-here"
```

Alternatively, you can set it as an environment variable:

```bash
export OPENROUTER_API_KEY="your-openrouter-api-key"
export LOGO_DEV_TOKEN="your-logo-dev-token"
```

You can get an API key by signing up at [OpenRouter.ai](https://openrouter.ai/).

### 💼 Ideal For
Business analysts exploring industry use of AI

AI/ML enthusiasts tracking use case trends

Product teams benchmarking competitor applications

Educators showcasing real-world AI case studies

### 🤝 Contributing
We welcome all contributions! To get started:

```bash
# Fork the repo and clone it
git clone https://github.com/yourusername/ai-use-case-navigator.git
cd ai-use-case-navigator
Feel free to open issues or submit PRs 🚀
```

### 📄 License
This project is licensed under the MIT License.
See the LICENSE file for details.

### 📸 Demo (Optional)
Add a screenshot or GIF of the app in use:

### 🔗 Related
Streamlit Docs

Awesome AI Use Cases
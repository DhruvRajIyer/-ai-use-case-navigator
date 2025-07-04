# AI Use Case Navigator

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue)
![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-orange)
![AI Powered](https://img.shields.io/badge/AI%20Assistant-OpenRouter-red)
![Semantic Search](https://img.shields.io/badge/Semantic%20Search-SentenceTransformer-blueviolet)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-ff69b4)

**Problem Statement:**  
Despite the widespread adoption of AI across industries, discovering and exploring real-world use cases remains fragmented. Researchers, business leaders, and developers lack a centralized, interactive platform to benchmark, analyze, and draw inspiration from successful AI implementations.

**Solution:**  
**AI Use Case Navigator** is a Streamlit-based application that curates and showcases practical AI use cases from real companies, enabling keyword and semantic search, rich filtering, and an AI-powered assistant to explore insights interactively.

---

## 📸 Demo

![AI Use Case Navigator Demo](assets/Demo.png)

---

## 🔧 Key Features

- **🔍 Keyword & Semantic Search**  
  Find use cases by company, domain, or using SentenceTransformer-based similarity search (FAISS).

- **🧠 Filter by Business Function & AI Type**  
  Easily explore AI trends across domains like HR, Finance, Healthcare, and more.

- **💬 AI Assistant**  
  OpenRouter-powered assistant answers natural language queries about use cases.

- **📊 Interactive Dashboard**  
  Clean UI with searchable tables, expandable cards, source links, and company logos.

- **⚡ Fast & Cached Loading**  
  Optimized for performance with local caching and index-based retrieval.

---

## 🧱 Tech Stack

| Layer             | Technologies Used                                                                 |
|------------------|------------------------------------------------------------------------------------|
| Frontend (UI)      | **Streamlit**, custom theming, interactive widgets                                 |
| Backend            | **Pandas**, **FAISS**, **SentenceTransformers**, **OpenRouter API**                |
| AI Integration	   |   - Semantic Embeddings via all-MiniLM-L6-v2 (SentenceTransformer)                 |
|                    |   - Natural Language QA via OpenRouter API                                        |
| Data Processing	   | CSV ingestion, deduplication, standardization, slug generation, data cleaning      |
| Storage & Caching	 | Embedding caching and FAISS index stored locally using Python Pickle for performance |
---

## 🔌 External API Integrations

- **OpenRouter API** – Powers the AI assistant that responds to user questions contextually.
- **Logo.dev API** – Dynamically fetches and displays company logos in the UI.

---

## 📂 Data Schema

Data sourced from a cleaned CSV file:  
`Data/ai_use_case_navigator_cleaned.csv`

| Column                 | Description                         |
|------------------------|-------------------------------------|
| `company`              | Company implementing the AI         |
| `use_case_name`        | Title of the AI use case            |
| `business_function`    | Department or domain (e.g., HR)     |
| `ai_type`              | Type of AI (e.g., NLP, CV)          |
| `outcome`              | Key result or impact                |
| `source_link`          | URL to the original use case        |
| `*_slug`               | Slugified for filtering purposes    |

---

## 🧠 Example Use Cases

- Automating resume screening using NLP in HR  
- Predictive maintenance in manufacturing via computer vision  
- Customer churn prediction in telecom using supervised learning  

---

## 🛠️ Setup Instructions

**Requirements:** Python 3.12+

```bash
# One-command setup
chmod +x setup.sh && ./setup.sh

# OR manual setup
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

To use the AI Assistant and logos:
```bash
# Add your API keys in .streamlit/secrets.toml
OPENROUTER_API_KEY = "your-key"
LOGO_DEV_TOKEN = "your-token"
```

---

## 💼 Ideal Users

- AI researchers & students exploring trends
- Product managers and consultants benchmarking applications
- Educators teaching real-world AI deployments

---

## 🤝 Contributing

We welcome contributions and suggestions!

```bash
# Fork, clone, and contribute
git clone https://github.com/yourusername/ai-use-case-navigator.git
```

---

## 📄 License

Licensed under the [MIT License](LICENSE).
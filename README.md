# 🧠 AI Use Case Navigator

A professional-grade **Streamlit dashboard** that lets users explore **real-world AI use cases** across top companies and industries — categorized by AI type, business function, and outcome.

> Built as part of Dhruv Iyer’s AI for Business Transformation portfolio.

---

## 🚀 Features

- ✅ Searchable & filterable use case table
- ✅ Sidebar filters for **AI Type** and **Business Function**
- ✅ Embedded outcome + source link for each row
- ✅ CSV backend + slug columns for frontend filtering
- ✅ Fully built in **Python** and **Streamlit**

---

## 🗂️ Dataset Structure

Loaded from `Data/ai_use_case_navigator_cleaned.csv`  
Key columns:

| Column                   | Description                                                  |
|--------------------------|--------------------------------------------------------------|
| `company`                | Company that implemented the AI use case                     |
| `use_case_name`          | Short title of the AI initiative                             |
| `business_function`      | Function impacted (e.g., Marketing, HR, Supply Chain)        |
| `ai_type`                | Type of AI used (e.g., NLP, Computer Vision, Forecasting)    |
| `outcome`                | Business impact (e.g., cost savings, revenue growth)         |
| `source_link`            | Link to original article/report                              |
| `ai_type_slug`           | Lowercase tag for filtering                                  |
| `business_function_slug` | Lowercase tag for filtering                                  |

---

## 🛠 Installation Options

### ✅ Option 1: Basic Setup

```bash
git clone https://github.com/yourusername/ai-use-case-navigator.git
cd ai-use-case-navigator
pip install -r requirements.txt
streamlit run app.py
🧪 Option 2: One-Liner Setup Script
If you have setup.sh or .venv1:

bash
Copy
Edit
chmod +x setup.sh
./setup.sh
Or:

bash
Copy
Edit
chmod +x .venv1
./.venv1
🔧 Tech Stack
Python

Streamlit

Pandas

CSV-based metadata

Optional: OpenAI + FAISS (Phase 2)

💼 Who’s It For?
Digital Transformation Consultants

AI Strategists & Analysts

Business School Students

Product Managers exploring AI ROI

🔮 Future Enhancements (Phase 2)
 Add semantic search (via OpenAI + FAISS)

 Add company/industry filter

 Create industry-specific dashboards (e.g., Fashion, Mobility)

 Enable exporting use cases (JSON/PDF)

 Add expandable rows or modals for better UX

🧑‍💻 Author
Dhruv Iyer
MSc AI for Business Transformation
Passionate about real-world applications of AI in strategy, marketing, finance, and digital transformation.

🔗 LinkedIn

💻 GitHub

📌 Live Demo (Optional)
👉 Launch the App
Replace with your actual deployed app link

📄 License
MIT License — free to use, remix, and build upon with attribution.
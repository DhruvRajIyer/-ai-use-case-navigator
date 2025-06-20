## 🚀 AI Use Case Navigator

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b.svg)](https://streamlit.io/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/ai-use-case-navigator/pulls)
[![Last Commit](https://img.shields.io/github/last-commit/yourusername/ai-use-case-navigator)](https://github.com/yourusername/ai-use-case-navigator/commits)

A **Streamlit** application that showcases real-world **AI use cases** across various industries and companies. Ideal for researchers, students, business leaders, and tech enthusiasts seeking inspiration or benchmarking examples.

---

## 🌟 Features

- 🔍 **Search** by company or use case name  
- 🧠 **Filter** by Business Function and AI Type  
- 📊 **Interactive table** with source links for each entry  
- 📁 Loads data from a clean CSV file  
- 💡 Highlights use case outcomes and AI adoption trends

---

## 🛠️ Setup & Usage

You can set up and run the application in multiple ways:

### ✅ Option 1: One-Click Setup Script

```bash
chmod +x setup.sh
./setup.sh
Creates a virtual environment, installs dependencies, and runs the app.

✅ Option 2: Using Makefile
bash
Copy
Edit
make setup     # Set up the environment and install dependencies
make run       # Launch the application
Other available commands:

make install – Install dependencies

make clean – Remove .venv and cached files

make help – Display help message

✅ Option 3: Manual Setup via .venv1
bash
Copy
Edit
chmod +x .venv1
./.venv1
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
✅ Option 4: Direct Installation
bash
Copy
Edit
pip install -r requirements.txt
streamlit run app.py
📊 Data Structure
The application reads from:

bash
Copy
Edit
Data/ai_use_case_navigator_cleaned.csv
Columns:
Column Name	Description
company	Organization using AI
use_case_name	Title of the AI use case
business_function	Related business domain (e.g., HR, Finance)
ai_type	Type of AI used (e.g., NLP, CV)
outcome	Key result or benefit
source_link	Link to the original article or report
ai_type_slug	Slugified AI type (for filtering)
business_function_slug	Slugified business function (for filtering)

📎 Requirements
Python 3.8+

Streamlit

Pandas
(Install everything using requirements.txt)

💼 Ideal For
Business analysts exploring industry use of AI

AI/ML enthusiasts tracking use case trends

Product teams benchmarking competitor applications

Educators showcasing real-world AI case studies

🤝 Contributing
We welcome all contributions! To get started:

bash
Copy
Edit
# Fork the repo and clone it
git clone https://github.com/yourusername/ai-use-case-navigator.git
cd ai-use-case-navigator
Feel free to open issues or submit PRs 🚀

📄 License
This project is licensed under the MIT License.
See the LICENSE file for details.

📸 Demo (Optional)
Add a screenshot or GIF of the app in use:

🔗 Related
Streamlit Docs

Awesome AI Use Cases
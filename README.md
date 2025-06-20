# AI Use Case Navigator

A Streamlit application that displays a searchable and filterable table of AI use cases across different companies and industries.

## Features

- Load and display AI use cases from CSV data
- Filter by Business Function
- Filter by AI Type
- Search by company name or use case name
- Interactive data table with source links

## Standardized Build Process

This project includes multiple ways to set up and run the application:

### Option 1: Using the setup script

```bash
# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

This will create a virtual environment, install dependencies, and start the application.

### Option 2: Using Make

```bash
# Set up the environment and install dependencies
make setup

# Run the application
make run
```

Other available make commands:
- `make install` - Install dependencies in the current environment
- `make clean` - Remove virtual environment and cached files
- `make help` - Show help message

### Option 3: Manual setup with .venv1

```bash
# Make the script executable
chmod +x .venv1

# Run the script to create a virtual environment
./.venv1

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Option 4: Direct installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Data Structure

The application uses data from `Data/ai_use_case_navigator_cleaned.csv` which contains the following columns:
- company
- use_case_name
- business_function
- ai_type
- outcome
- source_link
- ai_type_slug
- business_function_slug

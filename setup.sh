#!/bin/bash
# Setup script for AI Use Case Navigator
# This script creates a virtual environment, installs dependencies, and runs the app

# Configuration
VENV_NAME=".venv"
PYTHON_VERSION="python3.12"
REQUIREMENTS_FILE="requirements.txt"
APP_FILE="app.py"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v $PYTHON_VERSION &> /dev/null; then
    echo -e "${YELLOW}Python 3.12 not found. Please install Python 3.12 or higher.${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_NAME" ]; then
    echo -e "${GREEN}Creating virtual environment with Python 3.12...${NC}"
    $PYTHON_VERSION -m venv $VENV_NAME
    echo -e "${GREEN}Virtual environment created.${NC}"
else
    echo -e "${GREEN}Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source $VENV_NAME/bin/activate

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -r $REQUIREMENTS_FILE

# Run the application
echo -e "${GREEN}Starting Streamlit app...${NC}"
echo -e "${GREEN}Press Ctrl+C to stop the application${NC}"
streamlit run $APP_FILE

# Note: The virtual environment will remain active until you run 'deactivate'

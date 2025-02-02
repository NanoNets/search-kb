import os

# Create a virtual environment
os.system('python3 -m venv venv')

# Activate the virtual environment
os.system('source venv/bin/activate')

# Install necessary packages
os.system('pip install slack_sdk transformers torch')

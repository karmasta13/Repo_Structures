"""
WARIS Water Management Dashboard
Main entry point for Streamlit Community Cloud deployment
"""

import streamlit as st
import sys
import os

# Add the Multi_page directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Streamlit-Demo', 'Multi_page'))

# Import and run the Home.py file
if __name__ == "__main__":
    # Change to the Multi_page directory
    os.chdir(os.path.join(os.path.dirname(__file__), 'Streamlit-Demo', 'Multi_page'))
    
    # Import and run the main dashboard
    import Home

#!/bin/bash

# Local Streamlit Dashboard Runner
echo "🌊 Starting WARIS Water Management Dashboard locally..."
echo "====================================================="

# Navigate to the correct directory
cd "$(dirname "$0")/Streamlit-Demo/Multi_page"

# Check if data file exists
if [ ! -f "../../Data/WARIS.csv" ]; then
    echo "⚠️  Warning: Data file not found at ../../Data/WARIS.csv"
    echo "Please ensure your data file is in the correct location."
fi

# Run Streamlit
echo "🚀 Starting Streamlit server..."
echo "Dashboard will be available at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run Home.py --server.port 8501 --server.address localhost

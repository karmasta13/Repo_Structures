#!/bin/bash

# WARIS Water Management Dashboard Deployment Script
echo "🚀 WARIS Water Management Dashboard Deployment Script"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git branch -M main
fi

# Add all files
echo "📁 Adding files to Git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Deploy WARIS Water Management Dashboard - $(date)"

# Check if remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  No remote repository found!"
    echo "Please create a GitHub repository and add it as origin:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Code pushed to GitHub successfully!"
echo ""
echo "🌐 Next steps for Streamlit Cloud deployment:"
echo "1. Go to https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Select your repository"
echo "5. Set main file path to: streamlit_app.py"
echo "6. Click 'Deploy!'"
echo ""
echo "🎉 Your dashboard will be live at: https://YOUR_APP_NAME.streamlit.app"

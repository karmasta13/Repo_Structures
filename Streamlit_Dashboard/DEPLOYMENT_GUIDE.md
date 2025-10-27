# 🚀 Streamlit Dashboard Deployment Guide

## **Option 1: Streamlit Community Cloud (Recommended - FREE)**

### **Step 1: Prepare Your Code**

1. **Create a GitHub repository** and push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - WARIS Water Management Dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Ensure your file structure looks like this:**
   ```
   Streamlit_Dashboard/
   ├── streamlit_app.py          # Main entry point
   ├── requirements.txt          # Dependencies
   ├── .streamlit/
   │   └── config.toml           # Streamlit configuration
   ├── Streamlit-Demo/
   │   └── Multi_page/
   │       ├── Home.py           # Main dashboard
   │       └── pages/            # Other pages
   └── Data/
       └── WARIS.csv            # Your data file
   ```

### **Step 2: Deploy to Streamlit Cloud**

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with your GitHub account**
3. **Click "New app"**
4. **Fill in the details:**
   - **Repository**: `YOUR_USERNAME/YOUR_REPO_NAME`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. **Click "Deploy!"**

### **Step 3: Configure Environment**

In your Streamlit Cloud dashboard, add these secrets if needed:
```toml
[secrets]
# Add any API keys or sensitive data here
```

---

## **Option 2: Heroku (Paid)**

### **Step 1: Create Heroku Files**

Create `Procfile`:
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `runtime.txt`:
```
python-3.9.10
```

### **Step 2: Deploy to Heroku**

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-dashboard-name

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

---

## **Option 3: Docker (Self-hosted)**

### **Step 1: Create Dockerfile**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **Step 2: Build and Run**

```bash
# Build image
docker build -t waris-dashboard .

# Run container
docker run -p 8501:8501 waris-dashboard
```

---

## **Option 4: Local Network Sharing**

### **For Testing on Local Network**

```bash
# Run with network access
streamlit run Streamlit-Demo/Multi_page/Home.py --server.address 0.0.0.0 --server.port 8501
```

Then access from other devices using: `http://YOUR_IP:8501`

---

## **🔧 Troubleshooting**

### **Common Issues:**

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **Data File Not Found**: Ensure data files are in the repository
3. **Port Issues**: Use the correct port configuration
4. **Memory Issues**: Upgrade to a paid plan if needed

### **Performance Tips:**

1. **Use `@st.cache_data`** for data loading
2. **Optimize images** and reduce file sizes
3. **Use pagination** for large datasets
4. **Monitor memory usage**

---

## **📊 Monitoring Your Deployment**

### **Streamlit Cloud:**
- View logs in the dashboard
- Monitor usage and performance
- Easy redeployment on code changes

### **Heroku:**
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps
```

---

## **🔄 Updating Your App**

### **Streamlit Cloud:**
- Push changes to GitHub
- App automatically redeploys

### **Heroku:**
```bash
git add .
git commit -m "Update dashboard"
git push heroku main
```

---

## **💰 Cost Comparison**

| Platform | Cost | Ease | Features |
|----------|------|------|----------|
| Streamlit Cloud | FREE | ⭐⭐⭐⭐⭐ | Auto-deploy, easy setup |
| Heroku | $7+/month | ⭐⭐⭐⭐ | Full control, scaling |
| Docker | Varies | ⭐⭐⭐ | Complete control |
| Local | FREE | ⭐⭐ | Development only |

---

## **🎯 Recommended Approach**

**For Students/Learning**: Use **Streamlit Community Cloud** (FREE)
**For Production**: Use **Heroku** or **Docker**
**For Development**: Use **Local Network Sharing**

---

## **📞 Need Help?**

1. Check the [Streamlit documentation](https://docs.streamlit.io)
2. Visit [Streamlit Community](https://discuss.streamlit.io)
3. Check deployment logs for specific errors

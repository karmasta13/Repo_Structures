# 🎓 Streamlit Dashboard Teaching Guide

## 📚 **What is Streamlit?**

Streamlit is a Python library that makes it incredibly easy to create web applications for data science and machine learning. Think of it as a way to turn your Python scripts into interactive websites without needing to know HTML, CSS, or JavaScript!

### **Why Use Streamlit?**
- **Easy to Learn**: If you know Python, you can create web apps
- **No Web Development**: No need to learn HTML, CSS, or JavaScript
- **Interactive**: Create buttons, sliders, charts that users can interact with
- **Data Science Focused**: Perfect for dashboards, data analysis, and ML demos
- **Fast Development**: Create a working app in minutes, not hours

---

## 🚀 **Getting Started - Step by Step**

### **Step 1: Installation**

```bash
# Install Streamlit
pip install streamlit

# Or install from requirements.txt
pip install -r requirements.txt
```

### **Step 2: Your First Streamlit App**

Create a file called `my_first_app.py`:

```python
import streamlit as st

# This is the title of your app
st.title("My First Streamlit App!")

# This adds some text
st.write("Hello, World!")

# This creates a button
if st.button("Click me!"):
    st.write("Button was clicked!")
```

### **Step 3: Run Your App**

```bash
streamlit run my_first_app.py
```

**What happens?**
- Streamlit opens your web browser
- You see your app running at `http://localhost:8501`
- Every time you save your Python file, the app automatically updates!

---

## 🎨 **Understanding Our Dashboard Structure**

### **File Organization**
```
Streamlit_Dashboard/
├── website_dashboard.py          # Main dashboard (what we'll focus on)
├── requirements.txt              # Dependencies
├── TEACHING_GUIDE.md            # This guide
└── Data/
    └── WARIS.csv                # Our data file
```

### **Key Concepts in Our Dashboard**

#### **1. Page Configuration**
```python
st.set_page_config(
    page_title="WARIS Water Management Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)
```
**What this does:**
- Sets the browser tab title
- Adds an icon to the browser tab
- Makes the layout wide (uses full screen width)
- Hides the sidebar by default

#### **2. Custom Styling with CSS**
```python
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-radius: 0 0 20px 20px;
    }
</style>
""", unsafe_allow_html=True)
```
**What this does:**
- Adds custom CSS styling to make our app look professional
- Creates a beautiful gradient header
- Makes our dashboard look like a real website

#### **3. Data Loading with Caching**
```python
@st.cache_data
def load_data():
    df = pd.read_csv('../../Data/WARIS.csv')
    # ... data processing ...
    return df
```
**What this does:**
- `@st.cache_data` means Streamlit only loads the data once
- Makes the app much faster when users interact with it
- Data is cached in memory

#### **4. Navigation System**
```python
current_page = st.radio(
    "Navigation",
    ["Home", "Analytics", "Trends", "Data Explorer"],
    horizontal=True,
    label_visibility="collapsed"
)
```
**What this does:**
- Creates radio buttons for navigation
- `horizontal=True` makes them appear in a row
- `label_visibility="collapsed"` hides the label
- Users can click to switch between pages

#### **5. Conditional Content**
```python
if current_page == "Home":
    st.markdown('<div class="section-header">🏠 Dashboard Overview</div>')
    # ... home page content ...
elif current_page == "Analytics":
    st.markdown('<div class="section-header">📊 Advanced Analytics</div>')
    # ... analytics content ...
```
**What this does:**
- Shows different content based on which page is selected
- Like having multiple pages in one file

---

## 🛠️ **Key Streamlit Components We Use**

### **1. Text and Markdown**
```python
st.title("Main Title")           # Large title
st.header("Section Header")      # Medium header
st.subheader("Subsection")       # Small header
st.write("Regular text")         # Regular text
st.markdown("**Bold text**")     # Markdown formatting
```

### **2. Interactive Widgets**
```python
# Buttons
if st.button("Click me"):
    st.write("Button clicked!")

# Select boxes
option = st.selectbox("Choose an option", ["A", "B", "C"])

# Sliders
value = st.slider("Select a value", 0, 100, 50)

# Date inputs
date = st.date_input("Select a date")

# Multiselect
options = st.multiselect("Choose multiple", ["A", "B", "C"])
```

### **3. Data Display**
```python
# DataFrames
st.dataframe(df)                 # Interactive table
st.table(df)                     # Static table

# Charts (with Plotly)
import plotly.express as px
fig = px.line(df, x='date', y='value')
st.plotly_chart(fig)
```

### **4. Layout Components**
```python
# Columns
col1, col2 = st.columns(2)
with col1:
    st.write("Left column")
with col2:
    st.write("Right column")

# Expander (collapsible section)
with st.expander("Click to expand"):
    st.write("Hidden content")
```

---

## 🎯 **Teaching Script for Students**

### **Introduction (5 minutes)**
"Today we're going to learn how to create interactive web applications using Python and Streamlit. You don't need to know web development - just Python! We'll build a professional-looking dashboard that can analyze data, create charts, and let users interact with the information."

### **What We'll Build (2 minutes)**
"We're creating a water management dashboard that:
- Shows key performance indicators (KPIs)
- Displays interactive charts and graphs
- Allows users to filter data
- Has multiple pages for different types of analysis
- Looks professional with custom styling"

### **Key Learning Objectives (3 minutes)**
"By the end of this lesson, you'll understand:
1. How to create a basic Streamlit app
2. How to load and display data
3. How to create interactive widgets
4. How to make charts and visualizations
5. How to style your app to look professional
6. How to organize code for a multi-page application"

---

## 📖 **Detailed Step-by-Step Instructions**

### **Phase 1: Setup and Basic App (15 minutes)**

#### **Step 1.1: Install Streamlit**
```bash
pip install streamlit pandas plotly
```

#### **Step 1.2: Create Basic App**
Create `simple_dashboard.py`:
```python
import streamlit as st
import pandas as pd

st.title("My First Dashboard")
st.write("Welcome to my dashboard!")

# Load some data
data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
df = pd.DataFrame(data)

st.dataframe(df)
```

#### **Step 1.3: Run the App**
```bash
streamlit run simple_dashboard.py
```

**Student Activity:** "Try changing the data and see how the app updates automatically!"

### **Phase 2: Adding Interactivity (20 minutes)**

#### **Step 2.1: Add Interactive Elements**
```python
import streamlit as st
import pandas as pd

st.title("Interactive Dashboard")

# Add a slider
age_filter = st.slider("Minimum Age", 0, 50, 25)

# Add a selectbox
name_filter = st.selectbox("Choose a name", ["All", "Alice", "Bob", "Charlie"])

# Load data
data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
df = pd.DataFrame(data)

# Filter data based on inputs
if name_filter != "All":
    df = df[df['Name'] == name_filter]

df = df[df['Age'] >= age_filter]

st.dataframe(df)
```

**Student Activity:** "Try moving the slider and changing the dropdown. Notice how the table updates!"

### **Phase 3: Adding Charts (15 minutes)**

#### **Step 3.1: Create Visualizations**
```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Dashboard with Charts")

# Sample data
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Sales': [100, 120, 140, 110, 160],
    'Profit': [20, 30, 40, 25, 50]
}
df = pd.DataFrame(data)

# Create two columns
col1, col2 = st.columns(2)

with col1:
    # Bar chart
    fig = px.bar(df, x='Month', y='Sales', title='Sales by Month')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Line chart
    fig = px.line(df, x='Month', y='Profit', title='Profit Trend')
    st.plotly_chart(fig, use_container_width=True)
```

**Student Activity:** "Try hovering over the charts. Notice how interactive they are!"

### **Phase 4: Professional Styling (20 minutes)**

#### **Step 4.1: Add Custom CSS**
```python
import streamlit as st

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e40af, #3b82f6);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>Professional Dashboard</h1>
    <p>Beautiful styling with CSS</p>
</div>
""", unsafe_allow_html=True)

# Add some metric cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>Total Sales</h3>
        <h2>$1,234,567</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>Customers</h3>
        <h2>5,432</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>Growth</h3>
        <h2>+12.5%</h2>
    </div>
    """, unsafe_allow_html=True)
```

**Student Activity:** "Try changing the colors in the CSS. What happens?"

### **Phase 5: Multi-Page Navigation (25 minutes)**

#### **Step 5.1: Create Navigation System**
```python
import streamlit as st

# Navigation
page = st.radio("Navigate", ["Home", "Analytics", "Settings"], horizontal=True)

if page == "Home":
    st.title("Home Page")
    st.write("Welcome to the home page!")
    
elif page == "Analytics":
    st.title("Analytics Page")
    st.write("Here's your data analysis...")
    
elif page == "Settings":
    st.title("Settings Page")
    st.write("Configure your preferences...")
```

**Student Activity:** "Add a new page to the navigation. What do you need to add?"

---

## 🎯 **Common Student Questions & Answers**

### **Q: "Do I need to know HTML/CSS to use Streamlit?"**
**A:** No! Streamlit handles all the web development for you. You just write Python code, and Streamlit turns it into a website.

### **Q: "How do I make my app look more professional?"**
**A:** Use custom CSS (like we did in our dashboard), choose good colors, add proper spacing, and use consistent styling throughout.

### **Q: "Can I share my Streamlit app with others?"**
**A:** Yes! You can deploy it to Streamlit Cloud, Heroku, or other platforms. For now, others can access it if they're on the same network as you.

### **Q: "What if my data is too big?"**
**A:** Use `@st.cache_data` to cache your data, and consider sampling your data for display purposes.

### **Q: "How do I add more interactivity?"**
**A:** Use Streamlit's widgets like sliders, buttons, selectboxes, and checkboxes. You can also use Plotly charts which are naturally interactive.

---

## 🚀 **Advanced Concepts for Advanced Students**

### **1. Session State**
```python
# Initialize session state
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Use session state
if st.button('Increment'):
    st.session_state.counter += 1

st.write(f"Counter: {st.session_state.counter}")
```

### **2. File Uploads**
```python
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
```

### **3. Sidebar Usage**
```python
with st.sidebar:
    st.title("Controls")
    option = st.selectbox("Choose option", ["A", "B", "C"])
    st.slider("Value", 0, 100, 50)
```

---

## 📝 **Assignment Ideas**

### **Beginner Assignment**
Create a simple dashboard that:
- Loads a CSV file
- Shows the data in a table
- Has a filter (slider or selectbox)
- Displays one chart

### **Intermediate Assignment**
Create a dashboard that:
- Has multiple pages
- Uses custom styling
- Has multiple types of charts
- Includes interactive widgets
- Shows summary statistics

### **Advanced Assignment**
Create a dashboard that:
- Has professional branding
- Includes data export functionality
- Has advanced filtering options
- Uses session state
- Includes file upload capability

---

## 🎉 **Conclusion**

Streamlit makes it incredibly easy to create professional-looking web applications with just Python knowledge. The key is to:

1. **Start Simple**: Begin with basic components and gradually add complexity
2. **Use Styling**: Custom CSS makes a huge difference in appearance
3. **Think Interactive**: Add widgets and charts that users can interact with
4. **Organize Code**: Use functions and proper structure for larger apps
5. **Practice**: The more you build, the better you get!

**Remember:** Every professional dashboard started as a simple "Hello World" app. Start building and keep improving!

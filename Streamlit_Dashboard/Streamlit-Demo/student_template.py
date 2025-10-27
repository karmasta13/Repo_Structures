import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Student Dashboard Template",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for professional look
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
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 Student Dashboard Template</h1>
    <p>Your starting point for creating amazing dashboards!</p>
</div>
""", unsafe_allow_html=True)

# Sample data (replace with your own data)
@st.cache_data
def load_sample_data():
    """Load sample data for demonstration"""
    data = {
        'Date': pd.date_range('2023-01-01', periods=12, freq='M'),
        'Sales': [100, 120, 140, 110, 160, 180, 200, 190, 220, 240, 250, 280],
        'Profit': [20, 30, 40, 25, 50, 60, 70, 65, 80, 90, 95, 110],
        'Customers': [50, 60, 70, 55, 80, 90, 100, 95, 110, 120, 125, 140],
        'Region': ['North', 'South', 'East', 'West'] * 3
    }
    df = pd.DataFrame(data)
    return df

# Load data
df = load_sample_data()

# Navigation
st.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)
page = st.radio("Choose a page:", ["Overview", "Charts", "Data Table"], horizontal=True)

# Filters
st.markdown('<div class="section-header">Filters</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    # Date range filter
    start_date = st.date_input("Start Date", value=df['Date'].min().date())
    end_date = st.date_input("End Date", value=df['Date'].max().date())

with col2:
    # Region filter
    regions = st.multiselect("Select Regions", df['Region'].unique(), default=df['Region'].unique())
    # Metric selection
    metric = st.selectbox("Select Metric", ['Sales', 'Profit', 'Customers'])

# Apply filters
filtered_df = df[
    (df['Date'].dt.date >= start_date) & 
    (df['Date'].dt.date <= end_date) & 
    (df['Region'].isin(regions))
]

# Page content
if page == "Overview":
    st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
    
    # Calculate metrics
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_customers = filtered_df['Customers'].sum()
    avg_profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    
    # Display metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Sales</h3>
            <h2>${total_sales:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Profit</h3>
            <h2>${total_profit:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Customers</h3>
            <h2>{total_customers:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Profit Margin</h3>
            <h2>{avg_profit_margin:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)

elif page == "Charts":
    st.markdown('<div class="section-header">Data Visualizations</div>', unsafe_allow_html=True)
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"{metric} Over Time")
        fig = px.line(filtered_df, x='Date', y=metric, title=f'{metric} Trend')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(f"{metric} by Region")
        region_data = filtered_df.groupby('Region')[metric].sum().reset_index()
        fig = px.bar(region_data, x='Region', y=metric, title=f'{metric} by Region')
        st.plotly_chart(fig, use_container_width=True)
    
    # Full width chart
    st.subheader("Sales vs Profit Correlation")
    fig = px.scatter(filtered_df, x='Sales', y='Profit', color='Region', 
                     title='Sales vs Profit Relationship')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Data Table":
    st.markdown('<div class="section-header">Raw Data</div>', unsafe_allow_html=True)
    
    # Show filtered data
    st.write(f"Showing {len(filtered_df)} records")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 1rem;'>
    <p><strong>Student Dashboard Template</strong> | Built with Streamlit</p>
    <p>Replace the sample data with your own data to create your custom dashboard!</p>
</div>
""", unsafe_allow_html=True)

# Instructions for students
with st.expander("📚 Instructions for Students"):
    st.markdown("""
    ### How to Customize This Template:
    
    1. **Replace Sample Data**: 
       - Change the `load_sample_data()` function to load your own CSV file
       - Update column names to match your data
    
    2. **Add Your Own Metrics**:
       - Modify the metrics calculation in the Overview page
       - Add new KPI cards as needed
    
    3. **Create New Charts**:
       - Add more chart types in the Charts page
       - Use different Plotly chart types (pie, scatter, bar, etc.)
    
    4. **Add New Pages**:
       - Add new options to the radio button navigation
       - Create new `elif` blocks for each page
    
    5. **Customize Styling**:
       - Modify the CSS in the `st.markdown()` section
       - Change colors, fonts, and layout as needed
    
    ### Example: Loading Your Own Data
    ```python
    @st.cache_data
    def load_my_data():
        df = pd.read_csv('path/to/your/data.csv')
        return df
    ```
    
    ### Example: Adding a New Chart
    ```python
    fig = px.pie(df, values='column1', names='column2', title='My Pie Chart')
    st.plotly_chart(fig, use_container_width=True)
    ```
    """)

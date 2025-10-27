import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="WARIS Data Explorer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #3b82f6, #1d4ed8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #374151;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #3b82f6;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin: 0;
    }
    
    .data-table {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    """Load and preprocess the WARIS dataset"""
    try:
        df = pd.read_csv('../../../Data/WARIS.csv')
        df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY=1))
        df['Year'] = df['Date'].dt.year
        df['Month_Name'] = df['Date'].dt.month_name()
        df['Quarter'] = df['Date'].dt.quarter
        
        # Calculate additional metrics
        df['Net_Revenue'] = df['Total Operating Revenues'] - df['Total Operating Expenditures']
        df['Revenue_Growth'] = df.groupby('Zone')['Total Operating Revenues'].pct_change() * 100
        df['Efficiency_Score'] = (df['Collection Efficiency'] / 100) * df['Operation & Maintenance Cost Coverage']
        df['Collection_Rate'] = (df['Total Collection'] / df['Total Billing'] * 100).round(2)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load data
df = load_data()

if df.empty:
    st.error("No data available. Please check the data file path.")
    st.stop()

# Main content
st.markdown('<h1 class="main-header">📋 Data Explorer</h1>', unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.markdown("## 🎛️ Data Filters")
    
    # Date range filter
    st.markdown("### 📅 Date Range")
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Zone filter
    st.markdown("### 🏢 Zone Selection")
    all_zones = ['All'] + sorted(df['Zone'].unique().tolist())
    selected_zones = st.multiselect(
        "Select Zones",
        options=all_zones,
        default=['All']
    )
    
    # Year filter
    st.markdown("### 📊 Year Selection")
    years = sorted(df['Year'].unique())
    selected_years = st.multiselect(
        "Select Years",
        options=years,
        default=years
    )
    
    # Month filter
    st.markdown("### 📅 Month Selection")
    months = sorted(df['Month_Name'].unique())
    selected_months = st.multiselect(
        "Select Months",
        options=months,
        default=months
    )
    
    # Data view options
    st.markdown("### 📊 View Options")
    show_summary = st.checkbox("Show Summary Statistics", value=True)
    show_charts = st.checkbox("Show Data Visualizations", value=True)
    show_raw_data = st.checkbox("Show Raw Data Table", value=False)
    
    # Export options
    st.markdown("### 📥 Export Options")
    export_format = st.selectbox(
        "Export Format",
        options=['CSV', 'Excel', 'JSON']
    )

# Apply filters
filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['Date'].dt.date >= date_range[0]) & 
        (filtered_df['Date'].dt.date <= date_range[1])
    ]

if 'All' not in selected_zones:
    filtered_df = filtered_df[filtered_df['Zone'].isin(selected_zones)]

if selected_years:
    filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]

if selected_months:
    filtered_df = filtered_df[filtered_df['Month_Name'].isin(selected_months)]

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
    st.stop()

# Data Summary
if show_summary:
    st.markdown('<div class="section-header">📊 Data Summary</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(filtered_df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Records</div>
            <div class="metric-value">{total_records:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        unique_zones = filtered_df['Zone'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Zones Covered</div>
            <div class="metric-value">{unique_zones}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        date_span = (filtered_df['Date'].max() - filtered_df['Date'].min()).days
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Date Span (Days)</div>
            <div class="metric-value">{date_span}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_revenue = filtered_df['Total Operating Revenues'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">${total_revenue:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

# Data Visualizations
if show_charts:
    st.markdown('<div class="section-header">📈 Data Visualizations</div>', unsafe_allow_html=True)
    
    # Revenue and Expenditure Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Revenue by Zone
        revenue_by_zone = filtered_df.groupby('Zone')['Total Operating Revenues'].sum().reset_index()
        fig = px.bar(
            revenue_by_zone,
            x='Zone',
            y='Total Operating Revenues',
            title='Total Revenue by Zone',
            color='Total Operating Revenues',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="Zone",
            yaxis_title="Revenue ($)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Collection Efficiency by Zone
        efficiency_by_zone = filtered_df.groupby('Zone')['Collection Efficiency'].mean().reset_index()
        fig = px.bar(
            efficiency_by_zone,
            x='Zone',
            y='Collection Efficiency',
            title='Average Collection Efficiency by Zone',
            color='Collection Efficiency',
            color_continuous_scale='Plasma'
        )
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="Zone",
            yaxis_title="Collection Efficiency (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Time Series Analysis
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Revenue trends over time
    monthly_revenue = filtered_df.groupby(['Date', 'Zone'])['Total Operating Revenues'].sum().reset_index()
    fig = px.line(
        monthly_revenue,
        x='Date',
        y='Total Operating Revenues',
        color='Zone',
        title='Revenue Trends Over Time by Zone',
        markers=True
    )
    fig.update_layout(
        title_font_size=16,
        title_x=0.5,
        xaxis_title="Date",
        yaxis_title="Revenue ($)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Correlation Heatmap
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Select numeric columns for correlation
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    correlation_matrix = filtered_df[numeric_cols].corr()
    
    fig = px.imshow(
        correlation_matrix,
        text_auto=True,
        aspect="auto",
        title="Correlation Matrix of Numeric Variables",
        color_continuous_scale='RdBu'
    )
    fig.update_layout(
        title_font_size=16,
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Data Statistics
st.markdown('<div class="section-header">📈 Statistical Summary</div>', unsafe_allow_html=True)

# Descriptive statistics
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.subheader("Descriptive Statistics")
numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
stats_summary = filtered_df[numeric_cols].describe().round(2)
st.dataframe(stats_summary, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Zone-wise Summary
st.markdown('<div class="section-header">🏢 Zone-wise Summary</div>', unsafe_allow_html=True)

zone_summary = filtered_df.groupby('Zone').agg({
    'Total Operating Revenues': ['sum', 'mean', 'std'],
    'Total Operating Expenditures': ['sum', 'mean', 'std'],
    'Collection Efficiency': ['mean', 'std', 'min', 'max'],
    'Total Collection': ['sum', 'mean'],
    'Total Billing': ['sum', 'mean']
}).round(2)

# Flatten column names
zone_summary.columns = ['_'.join(col).strip() for col in zone_summary.columns]
zone_summary = zone_summary.reset_index()

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.dataframe(zone_summary, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Raw Data Table
if show_raw_data:
    st.markdown('<div class="section-header">📋 Raw Data Table</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Data Export
st.markdown('<div class="section-header">📥 Data Export</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if export_format == 'CSV':
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="📊 Download as CSV",
            data=csv_data,
            file_name=f"waris_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col2:
    if export_format == 'Excel':
        excel_data = filtered_df.to_excel(index=False)
        st.download_button(
            label="📊 Download as Excel",
            data=excel_data,
            file_name=f"waris_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with col3:
    if export_format == 'JSON':
        json_data = filtered_df.to_json(orient='records', indent=2)
        st.download_button(
            label="📊 Download as JSON",
            data=json_data,
            file_name=f"waris_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Data Quality Check
st.markdown('<div class="section-header">🔍 Data Quality Check</div>', unsafe_allow_html=True)

# Check for missing values
missing_data = filtered_df.isnull().sum()
missing_percentage = (missing_data / len(filtered_df)) * 100

quality_df = pd.DataFrame({
    'Column': missing_data.index,
    'Missing Values': missing_data.values,
    'Missing Percentage': missing_percentage.values
}).round(2)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.subheader("Missing Data Analysis")
st.dataframe(quality_df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6b7280; padding: 2rem;'>
        <p>📋 WARIS Data Explorer | Comprehensive Data Analysis</p>
        <p>Use the sidebar controls to filter and explore your data</p>
    </div>
    """,
    unsafe_allow_html=True
)
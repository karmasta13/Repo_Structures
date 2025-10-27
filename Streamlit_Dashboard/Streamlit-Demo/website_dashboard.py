import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="WARIS Water Management Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global CSS for consistent branding
st.markdown("""
<style>
    /* Global Brand Colors and Styles */
    :root {
        --primary-color: #1e40af;
        --secondary-color: #3b82f6;
        --accent-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --dark-color: #1f2937;
        --light-color: #f8fafc;
        --gray-color: #6b7280;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Custom Header */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        text-align: center;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Navigation Tabs */
    .nav-container {
        background: white;
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }
    
    .nav-tabs {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .nav-tab {
        background: white;
        border: 2px solid #e5e7eb;
        color: var(--gray-color);
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 1rem;
    }
    
    .nav-tab:hover {
        background: var(--light-color);
        border-color: var(--secondary-color);
        color: var(--secondary-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    
    .nav-tab.active {
        background: var(--secondary-color);
        color: white;
        border-color: var(--secondary-color);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: var(--dark-color);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid var(--secondary-color);
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 50px;
        height: 3px;
        background: var(--accent-color);
    }
    
    /* KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 5px solid var(--secondary-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(16, 185, 129, 0.1));
        border-radius: 0 15px 0 100px;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--dark-color);
        margin: 0.5rem 0;
        position: relative;
        z-index: 1;
    }
    
    .kpi-label {
        color: var(--gray-color);
        font-size: 1rem;
        margin: 0;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    .kpi-trend {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .trend-up { color: var(--accent-color); }
    .trend-down { color: var(--danger-color); }
    .trend-neutral { color: var(--gray-color); }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid #e5e7eb;
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--dark-color);
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* Filters */
    .filter-container {
        background: var(--light-color);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 1px solid #e5e7eb;
    }
    
    .filter-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--dark-color);
        margin-bottom: 1rem;
    }
    
    /* Data Tables */
    .data-table {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--secondary-color);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Footer */
    .footer {
        background: var(--dark-color);
        color: white;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
        border-radius: 15px 15px 0 0;
    }
    
    .footer p {
        margin: 0.5rem 0;
        opacity: 0.8;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .nav-tabs {
            flex-direction: column;
            align-items: center;
        }
        
        .nav-tab {
            width: 200px;
            text-align: center;
        }
        
        .kpi-container {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    """Load and preprocess the WARIS dataset"""
    try:
        df = pd.read_csv('../../Data/WARIS.csv')
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

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# Header
st.markdown("""
<div class="main-header">
    <h1>💧 WARIS Water Management Dashboard</h1>
    <p>Comprehensive Water Management Analytics & Insights</p>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("""
<div class="nav-container">
    <div class="nav-tabs">
        <div class="nav-tab" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'nav', value: 'Home'}, '*')">🏠 Home</div>
        <div class="nav-tab" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'nav', value: 'Analytics'}, '*')">📊 Analytics</div>
        <div class="nav-tab" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'nav', value: 'Trends'}, '*')">📈 Trends</div>
        <div class="nav-tab" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'nav', value: 'Data'}, '*')">📋 Data Explorer</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation using radio buttons (more reliable)
current_page = st.radio(
    "Navigation",
    ["Home", "Analytics", "Trends", "Data Explorer"],
    horizontal=True,
    label_visibility="collapsed",
    key="navigation"
)

# Filters (appear on all pages)
with st.expander("🔧 Filters & Controls", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Date range filter
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()
        date_range = st.date_input(
            "📅 Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    with col2:
        # Zone filter
        all_zones = ['All'] + sorted(df['Zone'].unique().tolist())
        selected_zones = st.multiselect(
            "🏢 Select Zones",
            options=all_zones,
            default=['All']
        )
    
    with col3:
        # Year filter
        years = sorted(df['Year'].unique())
        selected_years = st.multiselect(
            "📊 Select Years",
            options=years,
            default=years
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

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
    st.stop()

# Page Content
if current_page == "Home":
    st.markdown('<div class="section-header">🏠 Dashboard Overview</div>', unsafe_allow_html=True)
    
    # Key Performance Indicators
    total_revenue = filtered_df['Total Operating Revenues'].sum()
    total_expenditure = filtered_df['Total Operating Expenditures'].sum()
    net_revenue = total_revenue - total_expenditure
    avg_efficiency = filtered_df['Collection Efficiency'].mean()
    total_billing = filtered_df['Total Billing'].sum()
    total_collection = filtered_df['Total Collection'].sum()
    collection_rate = (total_collection / total_billing * 100) if total_billing > 0 else 0
    
    # Previous period comparison
    if len(filtered_df) > 1:
        prev_period_revenue = filtered_df.groupby('Year')['Total Operating Revenues'].sum().iloc[-2] if len(filtered_df.groupby('Year')) > 1 else 0
        revenue_growth = ((total_revenue - prev_period_revenue) / prev_period_revenue * 100) if prev_period_revenue > 0 else 0
    else:
        revenue_growth = 0
    
    # KPI Cards
    st.markdown("""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">${:,.0f}</div>
            <div class="kpi-trend trend-up">{:+.1f}% vs Previous Period</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Net Revenue</div>
            <div class="kpi-value">{:,.0f}</div>
            <div class="kpi-trend">Revenue - Expenditure</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Collection Efficiency</div>
            <div class="kpi-value">{:.1f}%</div>
            <div class="kpi-trend">Average across all zones</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Collection Rate</div>
            <div class="kpi-value">{:.1f}%</div>
            <div class="kpi-trend">Collections / Billing</div>
        </div>
    </div>
    """.format(total_revenue, revenue_growth, net_revenue, avg_efficiency, collection_rate), unsafe_allow_html=True)
    
    # Overview Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Revenue vs Expenditure Trends</div>', unsafe_allow_html=True)
        fig = px.line(
            filtered_df, 
            x='Date', 
            y=['Total Operating Revenues', 'Total Operating Expenditures'],
            title='',
            color_discrete_map={
                'Total Operating Revenues': '#10b981',
                'Total Operating Expenditures': '#ef4444'
            }
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Amount ($)",
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Revenue Distribution by Zone</div>', unsafe_allow_html=True)
        zone_revenue = filtered_df.groupby('Zone')['Total Operating Revenues'].sum().reset_index()
        fig = px.pie(
            zone_revenue, 
            values='Total Operating Revenues', 
            names='Zone',
            title='',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif current_page == "Analytics":
    st.markdown('<div class="section-header">📊 Advanced Analytics</div>', unsafe_allow_html=True)
    
    # Zone Performance Comparison
    zone_metrics = filtered_df.groupby('Zone').agg({
        'Total Operating Revenues': 'sum',
        'Total Operating Expenditures': 'sum',
        'Collection Efficiency': 'mean',
        'Operation & Maintenance Cost Coverage': 'mean',
        'Total Collection': 'sum',
        'Total Billing': 'sum'
    }).round(2)
    
    zone_metrics['Net Revenue'] = zone_metrics['Total Operating Revenues'] - zone_metrics['Total Operating Expenditures']
    zone_metrics['Collection Rate'] = (zone_metrics['Total Collection'] / zone_metrics['Total Billing'] * 100).round(2)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Zone Performance Summary</div>', unsafe_allow_html=True)
    st.dataframe(
        zone_metrics.style.format({
            'Total Operating Revenues': '${:,.0f}',
            'Total Operating Expenditures': '${:,.0f}',
            'Net Revenue': '${:,.0f}',
            'Collection Efficiency': '{:.1f}%',
            'Operation & Maintenance Cost Coverage': '{:.1f}%',
            'Collection Rate': '{:.1f}%',
            'Total Collection': '${:,.0f}',
            'Total Billing': '${:,.0f}'
        }),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Revenue Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Revenue by Zone Over Time</div>', unsafe_allow_html=True)
        revenue_data = filtered_df.groupby(['Zone', 'Year'])['Total Operating Revenues'].sum().reset_index()
        fig = px.bar(
            revenue_data,
            x='Year',
            y='Total Operating Revenues',
            color='Zone',
            title='',
            barmode='group'
        )
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Revenue ($)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Collection Efficiency Trends</div>', unsafe_allow_html=True)
        fig = px.line(
            filtered_df,
            x='Date',
            y='Collection Efficiency',
            color='Zone',
            title=''
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Collection Efficiency (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif current_page == "Trends":
    st.markdown('<div class="section-header">📈 Trends Analysis</div>', unsafe_allow_html=True)
    
    # Aggregation level selector
    agg_level = st.selectbox(
        "Select Aggregation Level",
        options=['Monthly', 'Quarterly', 'Yearly'],
        key="agg_level"
    )
    
    # Aggregate data based on selected level
    if agg_level == 'Monthly':
        agg_df = filtered_df.groupby(['Date', 'Zone']).agg({
            'Total Operating Revenues': 'sum',
            'Total Operating Expenditures': 'sum',
            'Collection Efficiency': 'mean',
            'Total Collection': 'sum',
            'Total Billing': 'sum',
            'Net_Revenue': 'sum'
        }).reset_index()
        x_col = 'Date'
    elif agg_level == 'Quarterly':
        agg_df = filtered_df.groupby(['Year', 'Quarter', 'Zone']).agg({
            'Total Operating Revenues': 'sum',
            'Total Operating Expenditures': 'sum',
            'Collection Efficiency': 'mean',
            'Total Collection': 'sum',
            'Total Billing': 'sum',
            'Net_Revenue': 'sum'
        }).reset_index()
        agg_df['Quarter_Date'] = pd.to_datetime(agg_df[['Year', 'Quarter']].assign(Month=agg_df['Quarter']*3))
        x_col = 'Quarter_Date'
    else:  # Yearly
        agg_df = filtered_df.groupby(['Year', 'Zone']).agg({
            'Total Operating Revenues': 'sum',
            'Total Operating Expenditures': 'sum',
            'Collection Efficiency': 'mean',
            'Total Collection': 'sum',
            'Total Billing': 'sum',
            'Net_Revenue': 'sum'
        }).reset_index()
        agg_df['Year_Date'] = pd.to_datetime(agg_df['Year'], format='%Y')
        x_col = 'Year_Date'
    
    # Revenue Trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Revenue Trends by Zone</div>', unsafe_allow_html=True)
        fig = px.line(
            agg_df,
            x=x_col,
            y='Total Operating Revenues',
            color='Zone',
            title='',
            markers=True
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Revenue ($)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Collection Efficiency Trends</div>', unsafe_allow_html=True)
        fig = px.line(
            agg_df,
            x=x_col,
            y='Collection Efficiency',
            color='Zone',
            title='',
            markers=True
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Collection Efficiency (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif current_page == "Data Explorer":
    st.markdown('<div class="section-header">📋 Data Explorer</div>', unsafe_allow_html=True)
    
    # Data Summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(filtered_df)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Records</div>
            <div class="kpi-value">{total_records:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        unique_zones = filtered_df['Zone'].nunique()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Zones Covered</div>
            <div class="kpi-value">{unique_zones}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        date_span = (filtered_df['Date'].max() - filtered_df['Date'].min()).days
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Date Span (Days)</div>
            <div class="kpi-value">{date_span}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_revenue = filtered_df['Total Operating Revenues'].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">${total_revenue:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Data Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Revenue by Zone</div>', unsafe_allow_html=True)
        revenue_by_zone = filtered_df.groupby('Zone')['Total Operating Revenues'].sum().reset_index()
        fig = px.bar(
            revenue_by_zone,
            x='Zone',
            y='Total Operating Revenues',
            title='',
            color='Total Operating Revenues',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            xaxis_title="Zone",
            yaxis_title="Revenue ($)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Collection Efficiency by Zone</div>', unsafe_allow_html=True)
        efficiency_by_zone = filtered_df.groupby('Zone')['Collection Efficiency'].mean().reset_index()
        fig = px.bar(
            efficiency_by_zone,
            x='Zone',
            y='Collection Efficiency',
            title='',
            color='Collection Efficiency',
            color_continuous_scale='Plasma'
        )
        fig.update_layout(
            xaxis_title="Zone",
            yaxis_title="Collection Efficiency (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Raw Data Table
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Raw Data Table</div>', unsafe_allow_html=True)
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Export Options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="📊 Download as CSV",
            data=csv_data,
            file_name=f"waris_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("""
<div class="footer">
    <p><strong>💧 WARIS Water Management Dashboard</strong></p>
    <p>Built with Streamlit | Data last updated: {}</p>
    <p>Professional Water Management Analytics & Insights</p>
</div>
""".format(datetime.now().strftime("%B %d, %Y at %I:%M %p")), unsafe_allow_html=True)

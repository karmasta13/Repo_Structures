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
    page_title="WARIS Water Management Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global CSS for water-themed branding
st.markdown("""
<style>
    /* Global Water-Themed Brand Colors */
    :root {
        --water-primary: #0ea5e9;      /* Sky blue */
        --water-secondary: #0284c7;    /* Deep blue */
        --water-accent: #06b6d4;       /* Cyan */
        --water-light: #e0f2fe;        /* Light blue */
        --water-dark: #0c4a6e;         /* Dark blue */
        --success-color: #10b981;      /* Green for positive metrics */
        --warning-color: #f59e0b;      /* Orange for warnings */
        --danger-color: #ef4444;       /* Red for negative metrics */
        --gray-color: #6b7280;         /* Gray for text */
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Water-themed Header */
    .main-header {
        background: linear-gradient(135deg, var(--water-primary) 0%, var(--water-secondary) 50%, var(--water-accent) 100%);
        padding: 3rem 0;
        margin-bottom: 2rem;
        border-radius: 0 0 25px 25px;
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="wave" x="0" y="0" width="100" height="20" patternUnits="userSpaceOnUse"><path d="M0,10 Q25,0 50,10 T100,10 V20 H0 Z" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23wave)"/></svg>') repeat-x;
        animation: wave 10s linear infinite;
    }
    
    @keyframes wave {
        0% { transform: translateX(0); }
        100% { transform: translateX(100px); }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        text-align: center;
        font-size: 1.3rem;
        margin: 0.5rem 0 0 0;
        position: relative;
        z-index: 1;
    }
    
    /* Navigation Tabs */
    .nav-container {
        background: white;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.1);
        border: 2px solid var(--water-light);
    }
    
    .nav-tabs {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .nav-tab {
        background: white;
        border: 2px solid var(--water-light);
        color: var(--water-dark);
        padding: 1rem 2rem;
        border-radius: 15px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 1.1rem;
        position: relative;
        overflow: hidden;
    }
    
    .nav-tab::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(14, 165, 233, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .nav-tab:hover::before {
        left: 100%;
    }
    
    .nav-tab:hover {
        background: var(--water-light);
        border-color: var(--water-primary);
        color: var(--water-primary);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.2);
    }
    
    .nav-tab.active {
        background: linear-gradient(135deg, var(--water-primary), var(--water-secondary));
        color: white;
        border-color: var(--water-primary);
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.3);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--water-dark);
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.8rem;
        border-bottom: 4px solid var(--water-primary);
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 60px;
        height: 4px;
        background: var(--water-accent);
        border-radius: 2px;
    }
    
    /* KPI Cards with Water Theme */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-bottom: 3rem;
    }
    
    .kpi-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.1);
        border-left: 6px solid var(--water-primary);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 120px;
        height: 120px;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(6, 182, 212, 0.1));
        border-radius: 0 20px 0 120px;
    }
    
    .kpi-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(14, 165, 233, 0.2);
        border-left-color: var(--water-accent);
    }
    
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 800;
        color: var(--water-dark);
        margin: 0.8rem 0;
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
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.8rem;
        position: relative;
        z-index: 1;
    }
    
    .trend-up { color: var(--success-color); }
    .trend-down { color: var(--danger-color); }
    .trend-neutral { color: var(--gray-color); }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.1);
        margin-bottom: 2rem;
        border: 1px solid var(--water-light);
        position: relative;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--water-primary), var(--water-accent));
        border-radius: 20px 20px 0 0;
    }
    
    .chart-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--water-dark);
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--water-light);
    }
    
    /* Filters with orange theme */
    .filter-container {
        background: #fef3c7;  /* Light orange background */
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 2px solid #f97316;  /* Orange border */
    }
    
    .filter-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--water-dark);
        margin-bottom: 1.5rem;
    }
    
    /* Data Tables */
    .data-table {
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.1);
        overflow: hidden;
        border: 1px solid var(--water-light);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--water-primary), var(--water-secondary));
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--water-secondary), var(--water-dark));
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4);
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, var(--water-dark) 0%, var(--water-secondary) 100%);
        color: white;
        padding: 3rem;
        text-align: center;
        margin-top: 4rem;
        border-radius: 25px 25px 0 0;
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="water" x="0" y="0" width="100" height="20" patternUnits="userSpaceOnUse"><path d="M0,10 Q25,0 50,10 T100,10 V20 H0 Z" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23water)"/></svg>') repeat-x;
    }
    
    .footer p {
        margin: 0.8rem 0;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* Style multiselect with orange theme */
    .stMultiSelect > div > div > div {
        background-color: #f97316 !important;  /* Orange background */
        color: white !important;
        border: 1px solid #f97316 !important;
    }
    
    .stMultiSelect > div > div > div > span {
        color: white !important;
    }
    
    .stMultiSelect > div > div > div > button {
        color: white !important;
    }
    
    /* Style multiselect container */
    .stMultiSelect > div > div {
        background-color: white;
        border: 2px solid #f97316;  /* Orange border */
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    /* Style date input with orange theme */
    .stDateInput > div > div {
        background-color: white;
        border: 2px solid #f97316;  /* Orange border */
        border-radius: 10px;
    }
    
    /* Style expander header with orange theme */
    .streamlit-expanderHeader {
        background-color: #f97316 !important;  /* Orange background */
        color: white !important;
        border-radius: 10px 10px 0 0;
    }
    
    .streamlit-expanderContent {
        background-color: white;
        border: 2px solid #f97316;  /* Orange border */
        border-top: none;
        border-radius: 0 0 10px 10px;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2.5rem;
        }
        
        .nav-tabs {
            flex-direction: column;
            align-items: center;
        }
        
        .nav-tab {
            width: 250px;
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
        df = pd.read_csv('../../../Data/WARIS.csv')
        df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY=1))
        df['Year'] = df['Date'].dt.year
        df['Month_Name'] = df['Date'].dt.month_name()
        
        # Calculate additional metrics
        df['Net_Revenue'] = df['Total Operating Revenues'] - df['Total Operating Expenditures']
        df['Revenue_Growth'] = df.groupby('Zone')['Total Operating Revenues'].pct_change() * 100
        df['Efficiency_Score'] = (df['Collection Efficiency'] / 100) * df['Operation & Maintenance Cost Coverage']
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load data
df = load_data()

if df.empty:
    st.error("No data available. Please check the data file path.")
    st.stop()

# Header
st.markdown("""
<div class="main-header">
    <h1>💧 WARIS Water Management Dashboard</h1>
    <p>Comprehensive Water Management Analytics & Insights</p>
</div>
""", unsafe_allow_html=True)

# Removed duplicate navigation - using only the functional buttons below

# Initialize session state for current page FIRST
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Home"

current_page = st.session_state.current_page

# Create clickable navigation buttons with active state styling
col1, col2, col3, col4 = st.columns(4)

with col1:
    button_type = "primary" if current_page == "🏠 Home" else "secondary"
    if st.button("🏠 Home", key="nav_home", use_container_width=True, type=button_type):
        st.session_state.current_page = "🏠 Home"
        st.rerun()

with col2:
    button_type = "primary" if current_page == "📊 Analytics" else "secondary"
    if st.button("📊 Analytics", key="nav_analytics", use_container_width=True, type=button_type):
        st.session_state.current_page = "📊 Analytics"
        st.rerun()

with col3:
    button_type = "primary" if current_page == "📈 Trends" else "secondary"
    if st.button("📈 Trends", key="nav_trends", use_container_width=True, type=button_type):
        st.session_state.current_page = "📈 Trends"
        st.rerun()

with col4:
    button_type = "primary" if current_page == "📋 Data Explorer" else "secondary"
    if st.button("📋 Data Explorer", key="nav_data", use_container_width=True, type=button_type):
        st.session_state.current_page = "📋 Data Explorer"
        st.rerun()

# Filters (collapsible) - Only show on Home page
if "🏠 Home" in current_page:
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
else:
    # For other pages, use all data
    filtered_df = df.copy()

# Page Content - Show different content based on selection
if "🏠 Home" in current_page:
    # HIERARCHICAL DESIGN: Most Critical KPIs at the Top
    st.markdown('<div class="section-header">🎯 Executive Summary - Key Performance Indicators</div>', unsafe_allow_html=True)

    # Calculate KPIs with advanced metrics
    total_revenue = filtered_df['Total Operating Revenues'].sum()
    total_expenditure = filtered_df['Total Operating Expenditures'].sum()
    net_revenue = total_revenue - total_expenditure
    avg_efficiency = filtered_df['Collection Efficiency'].mean()
    total_billing = filtered_df['Total Billing'].sum()
    total_collection = filtered_df['Total Collection'].sum()
    collection_rate = (total_collection / total_billing * 100) if total_billing > 0 else 0
    
    # Advanced KPI calculations
    total_zones = filtered_df['Zone'].nunique()
    avg_revenue_per_zone = total_revenue / total_zones if total_zones > 0 else 0
    efficiency_variance = filtered_df['Collection Efficiency'].std()
    
    # Previous period comparison for trend analysis
    if len(filtered_df) > 1:
        prev_period_revenue = filtered_df.groupby('Year')['Total Operating Revenues'].sum().iloc[-2] if len(filtered_df.groupby('Year')) > 1 else 0
        revenue_growth = ((total_revenue - prev_period_revenue) / prev_period_revenue * 100) if prev_period_revenue > 0 else 0
    else:
        revenue_growth = 0

    # HIERARCHICAL KPI CARDS - Most Critical First
    st.markdown("""
    <div class="kpi-container">
        <div class="kpi-card" style="border-left: 6px solid #10b981;">
            <div class="kpi-label">💰 Total Revenue</div>
            <div class="kpi-value">${:,.0f}</div>
            <div class="kpi-trend trend-up">{:+.1f}% vs Previous Period</div>
        </div>
        <div class="kpi-card" style="border-left: 6px solid #0ea5e9;">
            <div class="kpi-label">📊 Net Revenue</div>
            <div class="kpi-value">{:,.0f}</div>
            <div class="kpi-trend">Revenue - Expenditure</div>
        </div>
        <div class="kpi-card" style="border-left: 6px solid #f59e0b;">
            <div class="kpi-label">⚡ Collection Efficiency</div>
            <div class="kpi-value">{:.1f}%</div>
            <div class="kpi-trend">±{:.1f}% variance across zones</div>
        </div>
        <div class="kpi-card" style="border-left: 6px solid #06b6d4;">
            <div class="kpi-label">🎯 Collection Rate</div>
            <div class="kpi-value">{:.1f}%</div>
            <div class="kpi-trend">Collections / Billing</div>
        </div>
    </div>
    """.format(total_revenue, revenue_growth, net_revenue, avg_efficiency, efficiency_variance, collection_rate), unsafe_allow_html=True)
    
    # SECONDARY METRICS - Expandable Panel
    with st.expander("📈 Secondary Performance Metrics", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Avg Revenue per Zone", f"${avg_revenue_per_zone:,.0f}")
        with col2:
            st.metric("Total Zones", f"{total_zones}")
        with col3:
            st.metric("Total Billing", f"${total_billing:,.0f}")
        with col4:
            st.metric("Total Collection", f"${total_collection:,.0f}")

    # INTERACTIVE DRILL-DOWN CHARTS
    st.markdown('<div class="section-header">🔍 Interactive Data Exploration</div>', unsafe_allow_html=True)
    
    # Advanced Chart Controls
    chart_controls = st.container()
    with chart_controls:
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            chart_type = st.selectbox(
                "📊 Chart Type",
                ["Line Chart", "Bar Chart", "Area Chart"],
                key="chart_type"
            )
        
        with col2:
            aggregation = st.selectbox(
                "📅 Time Aggregation",
                ["Monthly", "Quarterly", "Yearly"],
                key="aggregation"
            )
        
        with col3:
            st.info("💡 **Tip**: Click on charts to drill down into specific data points!")
    
    # Revenue vs Expenditure over time with drill-down
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💰 Revenue vs Expenditure Trends (Click to Drill Down)</div>', unsafe_allow_html=True)
        
        # Apply aggregation
        if aggregation == "Monthly":
            chart_df = filtered_df.groupby(['Date', 'Zone']).agg({
                'Total Operating Revenues': 'sum',
                'Total Operating Expenditures': 'sum'
            }).reset_index()
        elif aggregation == "Quarterly":
            chart_df = filtered_df.copy()
            chart_df['Quarter'] = chart_df['Date'].dt.to_period('Q')
            chart_df = chart_df.groupby(['Quarter', 'Zone']).agg({
                'Total Operating Revenues': 'sum',
                'Total Operating Expenditures': 'sum'
            }).reset_index()
            chart_df['Date'] = chart_df['Quarter'].dt.start_time
        else:  # Yearly
            chart_df = filtered_df.groupby(['Year', 'Zone']).agg({
                'Total Operating Revenues': 'sum',
                'Total Operating Expenditures': 'sum'
            }).reset_index()
            chart_df['Date'] = pd.to_datetime(chart_df['Year'], format='%Y')
        
        # Create chart based on type
        if chart_type == "Line Chart":
            fig = px.line(
                chart_df, 
                x='Date', 
                y=['Total Operating Revenues', 'Total Operating Expenditures'],
                color='Zone',
                title='',
                color_discrete_map={
                    'Total Operating Revenues': '#0ea5e9',
                    'Total Operating Expenditures': '#ef4444'
                }
            )
        elif chart_type == "Bar Chart":
            fig = px.bar(
                chart_df, 
                x='Date', 
                y=['Total Operating Revenues', 'Total Operating Expenditures'],
                color='Zone',
                title='',
                barmode='group'
            )
        else:  # Area Chart
            fig = px.area(
                chart_df, 
              x='Date', 
              y=['Total Operating Revenues', 'Total Operating Expenditures'],
                color='Zone',
                title=''
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
        
        # Add click event for drill-down
        fig.update_traces(
            hovertemplate="<b>%{fullData.name}</b><br>" +
                         "Date: %{x}<br>" +
                         "Value: $%{y:,.0f}<br>" +
                         "<extra></extra>"
        )
        
        st.plotly_chart(fig, use_container_width=True, key="revenue_chart")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Interactive Zone Performance
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🏢 Zone Performance (Click to Filter)</div>', unsafe_allow_html=True)
        
        zone_revenue = filtered_df.groupby('Zone').agg({
            'Total Operating Revenues': 'sum',
            'Collection Efficiency': 'mean'
        }).reset_index()
        
        # Create interactive scatter plot
        fig = px.scatter(
            zone_revenue,
            x='Total Operating Revenues',
            y='Collection Efficiency',
            size='Total Operating Revenues',
            color='Zone',
            hover_name='Zone',
            hover_data={'Total Operating Revenues': ':.0f', 'Collection Efficiency': ':.1f'},
            title='',
            color_discrete_sequence=['#0ea5e9', '#0284c7', '#06b6d4', '#38bdf8', '#7dd3fc']
        )
        
        fig.update_layout(
            xaxis_title="Total Revenue ($)",
            yaxis_title="Collection Efficiency (%)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True, key="zone_scatter")
        st.markdown('</div>', unsafe_allow_html=True)

    # ADVANCED DRILL-DOWN: Zone Performance with Interactive Filtering
    st.markdown('<div class="section-header">🔍 Zone Performance Analysis (Drill-Down Enabled)</div>', unsafe_allow_html=True)
    
    # Interactive Zone Selection for Drill-Down
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        selected_zone = st.selectbox(
            "🎯 Select Zone for Detailed Analysis",
            ["All Zones"] + sorted(filtered_df['Zone'].unique().tolist()),
            key="zone_drill_down"
        )
    
    with col2:
        metric_focus = st.selectbox(
            "📊 Focus Metric",
            ["Revenue", "Efficiency", "Collection", "All Metrics"],
            key="metric_focus"
        )
    
    with col3:
        st.info("💡 **Drill-Down**: Select a specific zone to see detailed breakdown!")
    
    # Apply zone filter for drill-down
    if selected_zone != "All Zones":
        drill_down_df = filtered_df[filtered_df['Zone'] == selected_zone]
        st.success(f"🔍 **Drilling down into {selected_zone}** - Showing detailed analysis")
    else:
        drill_down_df = filtered_df
    
    # Calculate zone metrics
    zone_metrics = drill_down_df.groupby('Zone').agg({
        'Total Operating Revenues': 'sum',
        'Total Operating Expenditures': 'sum',
        'Collection Efficiency': 'mean',
        'Operation & Maintenance Cost Coverage': 'mean',
        'Total Collection': 'sum',
        'Total Billing': 'sum'
    }).round(2)

    zone_metrics['Net Revenue'] = zone_metrics['Total Operating Revenues'] - zone_metrics['Total Operating Expenditures']
    zone_metrics['Collection Rate'] = (zone_metrics['Total Collection'] / zone_metrics['Total Billing'] * 100).round(2)
    
    # Filter metrics based on focus
    if metric_focus == "Revenue":
        display_metrics = ['Total Operating Revenues', 'Total Operating Expenditures', 'Net Revenue']
    elif metric_focus == "Efficiency":
        display_metrics = ['Collection Efficiency', 'Operation & Maintenance Cost Coverage']
    elif metric_focus == "Collection":
        display_metrics = ['Total Collection', 'Total Billing', 'Collection Rate']
    else:
        display_metrics = zone_metrics.columns.tolist()
    
    # Display filtered metrics
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.dataframe(
        zone_metrics[display_metrics].style.format({
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
    
    # DRILL-DOWN: Detailed Zone Analysis
    if selected_zone != "All Zones":
        with st.expander(f"🔬 Deep Dive: {selected_zone} Detailed Analysis", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                # Monthly trend for selected zone
                monthly_trend = drill_down_df.groupby(drill_down_df['Date'].dt.to_period('M')).agg({
                    'Total Operating Revenues': 'sum',
                    'Collection Efficiency': 'mean'
                }).reset_index()
                monthly_trend['Date'] = monthly_trend['Date'].dt.start_time
                
                fig = px.line(
                    monthly_trend,
                    x='Date',
                    y=['Total Operating Revenues', 'Collection Efficiency'],
                    title=f'{selected_zone} Monthly Performance',
                    color_discrete_map={
                        'Total Operating Revenues': '#0ea5e9',
                        'Collection Efficiency': '#f59e0b'
                    }
                )
                fig.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Value"
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Performance comparison
                st.subheader(f"{selected_zone} vs All Zones")
                
                zone_avg = drill_down_df['Collection Efficiency'].mean()
                overall_avg = filtered_df['Collection Efficiency'].mean()
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric(
                        f"{selected_zone} Efficiency",
                        f"{zone_avg:.1f}%",
                        f"{(zone_avg - overall_avg):+.1f}% vs Average"
                    )
                with col_b:
                    st.metric(
                        "Overall Average",
                        f"{overall_avg:.1f}%"
                    )

    # ACTIONABLE INSIGHTS & ALERTS
    st.markdown('<div class="section-header">🚨 Actionable Insights & Alerts</div>', unsafe_allow_html=True)
    
    # Calculate insights
    best_zone = zone_metrics['Collection Efficiency'].idxmax()
    best_efficiency = zone_metrics['Collection Efficiency'].max()
    worst_zone = zone_metrics['Collection Efficiency'].idxmin()
    worst_efficiency = zone_metrics['Collection Efficiency'].min()
    highest_revenue_zone = zone_metrics['Total Operating Revenues'].idxmax()
    highest_revenue = zone_metrics['Total Operating Revenues'].max()
    total_zones = len(filtered_df['Zone'].unique())
    avg_revenue_per_zone = total_revenue / total_zones
    
    # Performance alerts
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance alerts
        st.markdown("### 🚨 Performance Alerts")
        
        if best_efficiency - worst_efficiency > 20:
            st.warning(f"⚠️ **High Performance Variance**: {best_zone} ({best_efficiency:.1f}%) vs {worst_zone} ({worst_efficiency:.1f}%) - Consider investigating {worst_zone}")
        
        if efficiency_variance > 15:
            st.error(f"🔴 **High Efficiency Variance**: {efficiency_variance:.1f}% - Inconsistent performance across zones")
        elif efficiency_variance < 5:
            st.success(f"✅ **Consistent Performance**: {efficiency_variance:.1f}% variance - Good operational consistency")
        
        if revenue_growth < 0:
            st.error(f"📉 **Revenue Decline**: {revenue_growth:.1f}% vs previous period - Immediate attention required")
        elif revenue_growth > 10:
            st.success(f"📈 **Strong Growth**: {revenue_growth:.1f}% vs previous period - Excellent performance")
    
    with col2:
        # Key insights
        st.markdown("### 💡 Key Insights")
        
        st.info(f"🏆 **Top Performer**: {best_zone} leads with {best_efficiency:.1f}% efficiency")
        st.info(f"💰 **Revenue Leader**: {highest_revenue_zone} generates ${highest_revenue:,.0f}")
        
        if collection_rate < 50:
            st.warning(f"⚠️ **Low Collection Rate**: {collection_rate:.1f}% - Review collection processes")
        else:
            st.success(f"✅ **Good Collection Rate**: {collection_rate:.1f}% - Healthy collection performance")
    
    # Executive Summary Cards
    st.markdown("### 📊 Executive Summary")
    st.markdown("""
    <div class="kpi-container">
        <div class="kpi-card" style="border-left: 6px solid #10b981;">
            <div class="kpi-label">🏆 Best Performing Zone</div>
            <div class="kpi-value">{}</div>
            <div class="kpi-trend">{:.1f}% Collection Efficiency</div>
        </div>
        <div class="kpi-card" style="border-left: 6px solid #0ea5e9;">
            <div class="kpi-label">💰 Highest Revenue Zone</div>
            <div class="kpi-value">{}</div>
            <div class="kpi-trend">${:,.0f}</div>
        </div>
        <div class="kpi-card" style="border-left: 6px solid #f59e0b;">
            <div class="kpi-label">📊 Average Revenue per Zone</div>
            <div class="kpi-value">${:,.0f}</div>
            <div class="kpi-trend">Across {} zones</div>
        </div>
        <div class="kpi-card" style="border-left: 6px solid #ef4444;">
            <div class="kpi-label">⚠️ Needs Attention</div>
            <div class="kpi-value">{}</div>
            <div class="kpi-trend">{:.1f}% Efficiency</div>
        </div>
    </div>
    """.format(best_zone, best_efficiency, highest_revenue_zone, highest_revenue, avg_revenue_per_zone, total_zones, worst_zone, worst_efficiency), unsafe_allow_html=True)

elif "📊 Analytics" in current_page:
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
    
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
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

elif "📈 Trends" in current_page:
    st.markdown('<div class="section-header">📈 Trends Analysis</div>', unsafe_allow_html=True)
    
    # Revenue trends over time
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Revenue Trends by Zone</div>', unsafe_allow_html=True)
        fig = px.line(
            filtered_df,
            x='Date',
            y='Total Operating Revenues',
            color='Zone',
            title=''
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

elif "📋 Data Explorer" in current_page:
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
    
    # Raw Data Table
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p><strong>💧 WARIS Water Management Dashboard</strong></p>
    <p>Built with Streamlit | Data last updated: {}</p>
    <p>Professional Water Management Analytics & Insights</p>
</div>
""".format(datetime.now().strftime("%B %d, %Y at %I:%M %p")), unsafe_allow_html=True)
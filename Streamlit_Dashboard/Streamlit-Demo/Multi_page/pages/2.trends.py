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
    page_title="WARIS Trends",
    page_icon="📈",
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
    
    .trend-up {
        color: #10b981;
    }
    
    .trend-down {
        color: #ef4444;
    }
    
    .trend-neutral {
        color: #6b7280;
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
st.markdown('<h1 class="main-header">📈 Trends Analysis</h1>', unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.markdown("## 🎛️ Trend Controls")
    
    # Date range selector
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
    
    # Trend type
    st.markdown("### 📊 Trend Type")
    trend_type = st.selectbox(
        "Select Trend Analysis Type",
        options=['Revenue Trends', 'Efficiency Trends', 'Expenditure Trends', 'Collection Trends', 'All Trends']
    )
    
    # Aggregation level
    st.markdown("### 📅 Aggregation Level")
    agg_level = st.selectbox(
        "Select Aggregation Level",
        options=['Monthly', 'Quarterly', 'Yearly']
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

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
    st.stop()

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
if trend_type in ['Revenue Trends', 'All Trends']:
    st.markdown('<div class="section-header">💰 Revenue Trends</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Revenue over time by zone
        fig = px.line(
            agg_df,
            x=x_col,
            y='Total Operating Revenues',
            color='Zone',
            title=f'Revenue Trends by Zone ({agg_level})',
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
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Revenue growth rate
        growth_data = agg_df.groupby('Zone')['Total Operating Revenues'].pct_change() * 100
        growth_df = agg_df.copy()
        growth_df['Growth_Rate'] = growth_data
        
        fig = px.bar(
            growth_df.dropna(),
            x=x_col,
            y='Growth_Rate',
            color='Zone',
            title=f'Revenue Growth Rate by Zone ({agg_level})',
            barmode='group'
        )
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Growth Rate (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Efficiency Trends
if trend_type in ['Efficiency Trends', 'All Trends']:
    st.markdown('<div class="section-header">⚡ Efficiency Trends</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Collection efficiency over time
        fig = px.line(
            agg_df,
            x=x_col,
            y='Collection Efficiency',
            color='Zone',
            title=f'Collection Efficiency Trends by Zone ({agg_level})',
            markers=True
        )
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Collection Efficiency (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Efficiency distribution
        fig = px.box(
            filtered_df,
            x='Zone',
            y='Collection Efficiency',
            title='Collection Efficiency Distribution by Zone',
            color='Zone'
        )
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="Zone",
            yaxis_title="Collection Efficiency (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Expenditure Trends
if trend_type in ['Expenditure Trends', 'All Trends']:
    st.markdown('<div class="section-header">💸 Expenditure Trends</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Expenditure over time
        fig = px.line(
            agg_df,
            x=x_col,
            y='Total Operating Expenditures',
            color='Zone',
            title=f'Expenditure Trends by Zone ({agg_level})',
            markers=True
        )
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Expenditure ($)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Revenue vs Expenditure scatter
        fig = px.scatter(
            agg_df,
            x='Total Operating Revenues',
            y='Total Operating Expenditures',
            color='Zone',
            size='Collection Efficiency',
            title='Revenue vs Expenditure by Zone',
            hover_data=['Collection Efficiency']
        )
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="Revenue ($)",
            yaxis_title="Expenditure ($)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Collection Trends
if trend_type in ['Collection Trends', 'All Trends']:
    st.markdown('<div class="section-header">📊 Collection Trends</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Collection vs Billing
        fig = px.line(
            agg_df,
            x=x_col,
            y=['Total Collection', 'Total Billing'],
            color='Zone',
            title=f'Collection vs Billing Trends by Zone ({agg_level})',
            markers=True
        )
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Amount ($)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Collection rate over time
        agg_df['Collection_Rate'] = (agg_df['Total Collection'] / agg_df['Total Billing'] * 100).round(2)
        fig = px.line(
            agg_df,
            x=x_col,
            y='Collection_Rate',
            color='Zone',
            title=f'Collection Rate Trends by Zone ({agg_level})',
            markers=True
        )
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Collection Rate (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Trend Summary Statistics
st.markdown('<div class="section-header">📈 Trend Summary Statistics</div>', unsafe_allow_html=True)

# Calculate trend statistics
trend_stats = agg_df.groupby('Zone').agg({
    'Total Operating Revenues': ['mean', 'std', 'min', 'max'],
    'Collection Efficiency': ['mean', 'std', 'min', 'max'],
    'Total Operating Expenditures': ['mean', 'std', 'min', 'max'],
    'Net_Revenue': ['mean', 'std', 'min', 'max']
}).round(2)

# Flatten column names
trend_stats.columns = ['_'.join(col).strip() for col in trend_stats.columns]
trend_stats = trend_stats.reset_index()

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.subheader(f"Trend Statistics by Zone ({agg_level})")
st.dataframe(trend_stats, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Zone Performance Comparison
st.markdown('<div class="section-header">🏆 Zone Performance Comparison</div>', unsafe_allow_html=True)

# Calculate performance metrics
performance_metrics = []
for zone in agg_df['Zone'].unique():
    zone_data = agg_df[agg_df['Zone'] == zone]
    
    # Calculate trends
    revenue_trend = zone_data['Total Operating Revenues'].pct_change().mean() * 100
    efficiency_trend = zone_data['Collection Efficiency'].pct_change().mean() * 100
    
    performance_metrics.append({
        'Zone': zone,
        'Avg Revenue': zone_data['Total Operating Revenues'].mean(),
        'Revenue Trend': revenue_trend,
        'Avg Efficiency': zone_data['Collection Efficiency'].mean(),
        'Efficiency Trend': efficiency_trend,
        'Total Net Revenue': zone_data['Net_Revenue'].sum()
    })

performance_df = pd.DataFrame(performance_metrics)

col1, col2, col3 = st.columns(3)

with col1:
    best_revenue_zone = performance_df.loc[performance_df['Avg Revenue'].idxmax()]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Highest Revenue Zone</div>
        <div class="metric-value">{best_revenue_zone['Zone']}</div>
        <div class="metric-label">${best_revenue_zone['Avg Revenue']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    best_efficiency_zone = performance_df.loc[performance_df['Avg Efficiency'].idxmax()]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Most Efficient Zone</div>
        <div class="metric-value">{best_efficiency_zone['Zone']}</div>
        <div class="metric-label">{best_efficiency_zone['Avg Efficiency']:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    best_net_zone = performance_df.loc[performance_df['Total Net Revenue'].idxmax()]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Best Net Revenue Zone</div>
        <div class="metric-value">{best_net_zone['Zone']}</div>
        <div class="metric-label">${best_net_zone['Total Net Revenue']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6b7280; padding: 2rem;'>
        <p>📈 WARIS Trends Dashboard | Comprehensive Trend Analysis</p>
        <p>Use the sidebar controls to customize your trend analysis</p>
    </div>
    """,
    unsafe_allow_html=True
)

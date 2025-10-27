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
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #3b82f6, #1d4ed8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #374151;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
    }
    
    .stSelectbox > div > div {
        background-color: #f8fafc;
        border-radius: 8px;
    }
    
    .stMultiSelect > div > div {
        background-color: #f8fafc;
        border-radius: 8px;
    }
    
    .stDateInput > div > div {
        background-color: #f8fafc;
        border-radius: 8px;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #3b82f6;
        transition: transform 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0.5rem 0;
    }
    
    .kpi-label {
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
        df = pd.read_csv('../../Data/WARIS.csv')
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

# Sidebar
with st.sidebar:
    st.markdown("## 🎛️ Dashboard Controls")
    
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

# Main content
st.markdown('<h1 class="main-header">💧 WARIS Water Management Dashboard</h1>', unsafe_allow_html=True)

# Key Performance Indicators
st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)

# Calculate KPIs
total_revenue = filtered_df['Total Operating Revenues'].sum()
total_expenditure = filtered_df['Total Operating Expenditures'].sum()
net_revenue = total_revenue - total_expenditure
avg_efficiency = filtered_df['Collection Efficiency'].mean()
total_billing = filtered_df['Total Billing'].sum()
total_collection = filtered_df['Total Collection'].sum()
collection_rate = (total_collection / total_billing * 100) if total_billing > 0 else 0

# Previous period comparison (if data available)
if len(filtered_df) > 1:
    prev_period_revenue = filtered_df.groupby('Year')['Total Operating Revenues'].sum().iloc[-2] if len(filtered_df.groupby('Year')) > 1 else 0
    revenue_growth = ((total_revenue - prev_period_revenue) / prev_period_revenue * 100) if prev_period_revenue > 0 else 0
else:
    revenue_growth = 0

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">${total_revenue:,.0f}</div>
        <div class="{'trend-up' if revenue_growth > 0 else 'trend-down' if revenue_growth < 0 else 'trend-neutral'}">
            {f"{revenue_growth:+.1f}%" if revenue_growth != 0 else "No change"}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Net Revenue</div>
        <div class="kpi-value {'trend-up' if net_revenue > 0 else 'trend-down'}">${net_revenue:,.0f}</div>
        <div class="kpi-label">Revenue - Expenditure</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Collection Efficiency</div>
        <div class="kpi-value">{avg_efficiency:.1f}%</div>
        <div class="kpi-label">Average across all zones</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Collection Rate</div>
        <div class="kpi-value">{collection_rate:.1f}%</div>
        <div class="kpi-label">Collections / Billing</div>
    </div>
    """, unsafe_allow_html=True)

# Charts Section
st.markdown('<div class="section-header">📈 Revenue & Expenditure Analysis</div>', unsafe_allow_html=True)

# Revenue vs Expenditure over time
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = px.line(
        filtered_df, 
        x='Date', 
        y=['Total Operating Revenues', 'Total Operating Expenditures'],
        title='Revenue vs Expenditure Trends',
        color_discrete_map={
            'Total Operating Revenues': '#10b981',
            'Total Operating Expenditures': '#ef4444'
        }
    )
    fig.update_layout(
        title_font_size=20,
        title_x=0.5,
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
    # Revenue by Zone Pie Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    zone_revenue = filtered_df.groupby('Zone')['Total Operating Revenues'].sum().reset_index()
    fig = px.pie(
        zone_revenue, 
        values='Total Operating Revenues', 
        names='Zone',
        title='Revenue Distribution by Zone',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_font_size=16, title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Zone Performance Analysis
st.markdown('<div class="section-header">🏢 Zone Performance Analysis</div>', unsafe_allow_html=True)

# Zone comparison metrics
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

# Display zone metrics table
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.subheader("Zone Performance Summary")
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

# Efficiency Analysis
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Collection Efficiency by Zone
    fig = px.bar(
        filtered_df.groupby('Zone')['Collection Efficiency'].mean().reset_index(),
        x='Zone',
        y='Collection Efficiency',
        title='Average Collection Efficiency by Zone',
        color='Collection Efficiency',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        title_font_size=16,
        title_x=0.5,
        xaxis_title="Zone",
        yaxis_title="Collection Efficiency (%)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Maintenance Cost Coverage
    fig = px.bar(
        filtered_df.groupby('Zone')['Operation & Maintenance Cost Coverage'].mean().reset_index(),
        x='Zone',
        y='Operation & Maintenance Cost Coverage',
        title='Average O&M Cost Coverage by Zone',
        color='Operation & Maintenance Cost Coverage',
        color_continuous_scale='Plasma'
    )
    fig.update_layout(
        title_font_size=16,
        title_x=0.5,
        xaxis_title="Zone",
        yaxis_title="O&M Cost Coverage (%)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Monthly Trends
st.markdown('<div class="section-header">📅 Monthly Trends Analysis</div>', unsafe_allow_html=True)

# Monthly revenue and expenditure trends
monthly_data = filtered_df.groupby(['Year', 'Month']).agg({
    'Total Operating Revenues': 'sum',
    'Total Operating Expenditures': 'sum',
    'Collection Efficiency': 'mean'
}).reset_index()

monthly_data['Date'] = pd.to_datetime(monthly_data[['Year', 'Month']].assign(DAY=1))
monthly_data['Net Revenue'] = monthly_data['Total Operating Revenues'] - monthly_data['Total Operating Expenditures']

# Create subplot for monthly trends
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Monthly Revenue vs Expenditure', 'Monthly Collection Efficiency'),
    vertical_spacing=0.1
)

# Revenue and Expenditure
fig.add_trace(
    go.Scatter(x=monthly_data['Date'], y=monthly_data['Total Operating Revenues'], 
               name='Revenue', line=dict(color='#10b981', width=3)),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=monthly_data['Date'], y=monthly_data['Total Operating Expenditures'], 
               name='Expenditure', line=dict(color='#ef4444', width=3)),
    row=1, col=1
)

# Collection Efficiency
fig.add_trace(
    go.Scatter(x=monthly_data['Date'], y=monthly_data['Collection Efficiency'], 
               name='Collection Efficiency', line=dict(color='#3b82f6', width=3)),
    row=2, col=1
)

fig.update_layout(
    height=600,
    title_text="Monthly Performance Trends",
    title_font_size=20,
    title_x=0.5,
    showlegend=True
)

fig.update_xaxes(title_text="Date", row=2, col=1)
fig.update_yaxes(title_text="Amount ($)", row=1, col=1)
fig.update_yaxes(title_text="Efficiency (%)", row=2, col=1)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Data Export Section
st.markdown('<div class="section-header">📥 Data Export</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    # Export filtered data
    csv_data = filtered_df.to_csv(index=False)
    st.download_button(
        label="📊 Download Filtered Data (CSV)",
        data=csv_data,
        file_name=f"waris_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col2:
    # Export zone summary
    zone_summary = zone_metrics.to_csv()
    st.download_button(
        label="🏢 Download Zone Summary (CSV)",
        data=zone_summary,
        file_name=f"zone_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col3:
    # Export monthly trends
    monthly_summary = monthly_data.to_csv(index=False)
    st.download_button(
        label="📅 Download Monthly Trends (CSV)",
        data=monthly_summary,
        file_name=f"monthly_trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6b7280; padding: 2rem;'>
        <p>💧 WARIS Water Management Dashboard | Built with Streamlit</p>
        <p>Data last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%B %d, %Y at %I:%M %p")),
    unsafe_allow_html=True
)

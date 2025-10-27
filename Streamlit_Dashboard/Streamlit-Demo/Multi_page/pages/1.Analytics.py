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
    page_title="WARIS Analytics",
    page_icon="📊",
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

# Main content
st.markdown('<h1 class="main-header">📊 Advanced Analytics</h1>', unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.markdown("## 🎛️ Analytics Controls")
    
    # Zone selector
    st.markdown("### 🏢 Zone Selection")
    selected_zones = st.multiselect(
        "Select Zones for Analysis",
        options=sorted(df['Zone'].unique()),
        default=sorted(df['Zone'].unique())[:2]
    )
    
    # Year range
    st.markdown("### 📅 Year Range")
    years = sorted(df['Year'].unique())
    year_range = st.select_slider(
        "Select Year Range",
        options=years,
        value=(years[0], years[-1])
    )
    
    # Metric selection
    st.markdown("### 📊 Metrics to Analyze")
    metrics = [
        'Total Operating Revenues',
        'Total Operating Expenditures',
        'Collection Efficiency',
        'Operation & Maintenance Cost Coverage',
        'Total Collection',
        'Total Billing'
    ]
    selected_metrics = st.multiselect(
        "Select Metrics",
        options=metrics,
        default=metrics[:3]
    )

# Filter data based on selections
filtered_df = df[
    (df['Zone'].isin(selected_zones)) & 
    (df['Year'] >= year_range[0]) & 
    (df['Year'] <= year_range[1])
]

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
    st.stop()

# Zone Performance Comparison
st.markdown('<div class="section-header">🏢 Zone Performance Comparison</div>', unsafe_allow_html=True)

# Calculate zone metrics
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

# Display zone comparison table
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

# Revenue Analysis
st.markdown('<div class="section-header">💰 Revenue Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Revenue by Zone and Year
    revenue_data = filtered_df.groupby(['Zone', 'Year'])['Total Operating Revenues'].sum().reset_index()
    fig = px.bar(
        revenue_data,
        x='Year',
        y='Total Operating Revenues',
        color='Zone',
        title='Revenue by Zone Over Time',
        barmode='group'
    )
    fig.update_layout(
        title_font_size=16,
        title_x=0.5,
        xaxis_title="Year",
        yaxis_title="Revenue ($)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Revenue distribution pie chart
    total_revenue_by_zone = filtered_df.groupby('Zone')['Total Operating Revenues'].sum().reset_index()
    fig = px.pie(
        total_revenue_by_zone,
        values='Total Operating Revenues',
        names='Zone',
        title='Revenue Distribution by Zone',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_font_size=16, title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Efficiency Analysis
st.markdown('<div class="section-header">⚡ Efficiency Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Collection Efficiency over time
    fig = px.line(
        filtered_df,
        x='Date',
        y='Collection Efficiency',
        color='Zone',
        title='Collection Efficiency Trends by Zone'
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
    # O&M Cost Coverage
    fig = px.bar(
        filtered_df.groupby('Zone')['Operation & Maintenance Cost Coverage'].mean().reset_index(),
        x='Zone',
        y='Operation & Maintenance Cost Coverage',
        title='Average O&M Cost Coverage by Zone',
        color='Operation & Maintenance Cost Coverage',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        title_font_size=16,
        title_x=0.5,
        xaxis_title="Zone",
        yaxis_title="O&M Cost Coverage (%)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Correlation Analysis
st.markdown('<div class="section-header">🔗 Correlation Analysis</div>', unsafe_allow_html=True)

# Calculate correlation matrix for selected metrics
if len(selected_metrics) > 1:
    correlation_data = filtered_df[selected_metrics + ['Zone']].groupby('Zone')[selected_metrics].corr()
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = px.imshow(
        correlation_data,
        text_auto=True,
        aspect="auto",
        title="Correlation Matrix of Selected Metrics by Zone",
        color_continuous_scale='RdBu'
    )
    fig.update_layout(
        title_font_size=16,
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Statistical Summary
st.markdown('<div class="section-header">📈 Statistical Summary</div>', unsafe_allow_html=True)

# Calculate statistics for selected metrics
stats_summary = filtered_df[selected_metrics].describe().round(2)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.subheader("Descriptive Statistics")
st.dataframe(stats_summary, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Zone-specific insights
st.markdown('<div class="section-header">💡 Zone-Specific Insights</div>', unsafe_allow_html=True)

for zone in selected_zones:
    zone_data = filtered_df[filtered_df['Zone'] == zone]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_revenue = zone_data['Total Operating Revenues'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{zone} - Avg Revenue</div>
            <div class="metric-value">${avg_revenue:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_efficiency = zone_data['Collection Efficiency'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{zone} - Avg Efficiency</div>
            <div class="metric-value">{avg_efficiency:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_collection = zone_data['Total Collection'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{zone} - Total Collection</div>
            <div class="metric-value">${total_collection:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6b7280; padding: 2rem;'>
        <p>📊 WARIS Analytics Dashboard | Advanced Data Analysis</p>
        <p>Use the sidebar controls to customize your analysis</p>
    </div>
    """,
    unsafe_allow_html=True
)
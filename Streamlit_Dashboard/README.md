# 💧 WARIS Water Management Dashboard

A comprehensive, modern Streamlit dashboard for analyzing water management data with beautiful UI and interactive visualizations.

## 🚀 Features

### 📊 Main Dashboard (`main_dashboard.py`)
- **Modern UI Design**: Clean, professional interface with custom CSS styling
- **Key Performance Indicators**: Real-time KPI cards with trend indicators
- **Interactive Charts**: Revenue vs Expenditure trends, zone comparisons, efficiency analysis
- **Advanced Filtering**: Date range, zone, and year-based filtering
- **Data Export**: Multiple export formats (CSV, Excel, JSON)
- **Responsive Layout**: Optimized for different screen sizes

### 🏠 Multi-Page Dashboard
- **Home Page**: Overview with key metrics and quick insights
- **Analytics Page**: Advanced data analysis with correlation matrices and statistical summaries
- **Trends Page**: Comprehensive trend analysis with multiple aggregation levels
- **Data Explorer**: Interactive data exploration with filtering and export options

## 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Dashboard**:
   ```bash
   # Single page dashboard
   streamlit run Streamlit-Demo/main_dashboard.py
   
   # Multi-page dashboard
   streamlit run Streamlit-Demo/Multi_page/Home.py
   ```

## 📁 Project Structure

```
Streamlit_Dashboard/
├── README.md
├── requirements.txt
└── Streamlit-Demo/
    ├── main_dashboard.py          # Main comprehensive dashboard
    ├── single_page_app.py         # Original single page app
    └── Multi_page/
        ├── Home.py                # Home page
        └── pages/
            ├── 1.Analytics.py     # Analytics page
            ├── 2.trends.py        # Trends page
            └── 3.data.py          # Data explorer page
```

## 🎨 UI Features

### Modern Design Elements
- **Gradient Headers**: Eye-catching gradient text effects
- **Card-based Layout**: Clean metric cards with hover effects
- **Custom Color Scheme**: Professional blue and green color palette
- **Responsive Grid**: Adaptive layout for different screen sizes
- **Interactive Elements**: Hover effects and smooth transitions

### Chart Types
- **Line Charts**: Time series trends
- **Bar Charts**: Comparative analysis
- **Pie Charts**: Distribution analysis
- **Scatter Plots**: Correlation analysis
- **Heatmaps**: Correlation matrices
- **Box Plots**: Distribution analysis

## 📊 Data Analysis Features

### Key Metrics
- Total Revenue and Expenditure
- Collection Efficiency
- Net Revenue calculations
- Growth rate analysis
- Zone performance comparison

### Interactive Controls
- Date range selection
- Zone filtering
- Year and month selection
- Metric selection for analysis
- Aggregation level selection (Monthly, Quarterly, Yearly)

### Export Options
- CSV export with custom naming
- Excel export with formatting
- JSON export for API integration
- Filtered data export

## 🔧 Customization

### Styling
The dashboard uses custom CSS for modern styling. Key classes include:
- `.main-header`: Gradient text headers
- `.metric-card`: KPI card styling
- `.chart-container`: Chart wrapper styling
- `.section-header`: Section dividers

### Data Source
Update the data path in the `load_data()` function:
```python
df = pd.read_csv('../../Data/WARIS.csv')
```

## 📈 Usage

1. **Launch the Dashboard**: Run the appropriate Streamlit command
2. **Filter Data**: Use sidebar controls to filter by date, zone, or year
3. **Explore Visualizations**: Interact with charts and tables
4. **Export Data**: Download filtered data in your preferred format
5. **Navigate Pages**: Use the multi-page navigation for different analysis views

## 🎯 Key Benefits

- **Professional Appearance**: Modern, clean UI that looks like a proper business dashboard
- **Interactive Analysis**: Real-time filtering and dynamic visualizations
- **Comprehensive Insights**: Multiple analysis perspectives in one dashboard
- **Data Export**: Easy data export for further analysis
- **Responsive Design**: Works on different screen sizes
- **Performance Optimized**: Cached data loading for better performance

## 🔮 Future Enhancements

- Real-time data updates
- User authentication
- Advanced predictive analytics
- Mobile app integration
- Real-time notifications
- Advanced reporting features

## 📝 Notes

- Ensure your data file is in the correct path (`../../Data/WARIS.csv`)
- The dashboard is optimized for the WARIS dataset structure
- All visualizations are interactive and responsive
- Data is cached for better performance

---

**Built with ❤️ using Streamlit, Plotly, and Pandas**
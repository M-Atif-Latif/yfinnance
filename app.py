import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Page Configuration
st.set_page_config(
    page_title="Global Markets Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
# st.markdown("""
# <style>
#     :root {
#         --primary-color: #2563eb;
#         --secondary-color: #1e40af;
#         --accent-color: #3b82f6;
#         --background-color: #f8fafc;
#         --surface-color: #ffffff;
#         --text-color: #1e293b;
#         --text-secondary: #64748b;
#     }
    
#     .main {
#         background-color: var(--background-color);
#         color: var(--text-color);
#     }
    
#     .stSelectbox div, .stTextInput div, .stDateInput div {
#         background-color: var(--surface-color) !important;
#         border-radius: 8px !important;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
#     }
    
#     .stButton>button {
#         background-color: var(--primary-color) !important;
#         color: white !important;
#         border-radius: 8px !important;
#         padding: 0.5rem 1rem !important;
#         font-weight: 500 !important;
#         transition: all 0.2s !important;
#     }
    
#     .stButton>button:hover {
#         background-color: var(--secondary-color) !important;
#         transform: translateY(-1px) !important;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
#     }
    
#     .stMetric {
#         background-color: var(--surface-color) !important;
#         border-radius: 12px !important;
#         padding: 1.5rem !important;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
#     }
    
#     .stDataFrame {
#         border-radius: 12px !important;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
#     }
    
#     .stTabs [aria-selected="true"] {
#         background-color: var(--primary-color) !important;
#         color: white !important;
#     }
    
#     .sidebar .sidebar-content {
#         background: linear-gradient(180deg, #2563eb 0%, #1e40af 100%) !important;
#         color: white !important;
#     }
    
#     .sidebar .sidebar-content a {
#         color: white !important;
#     }
    
#     .sidebar .sidebar-content .stMarkdown h1, 
#     .sidebar .sidebar-content .stMarkdown h2,
#     .sidebar .sidebar-content .stMarkdown h3 {
#         color: white !important;
#     }
# </style>
# """, unsafe_allow_html=True)

#just change the css becuse the css is so bright and not professional
# Custom CSS for dark theme
st.markdown("""
<style>
    :root {
        --primary-color: #1f2937; /* Dark Gray */
        --secondary-color: #4b5563; /* Medium Gray */
        --accent-color: #10b981; /* Emerald Green */
        --background-color: #111827; /* Dark Background */
        --surface-color: #1f2937; /* Surface Background */
        --text-color: #f9fafb; /* Light Text */
        --text-secondary: #9ca3af; /* Muted Text */
    }
    
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    .stSelectbox div, .stTextInput div, .stDateInput div {
        background-color: var(--surface-color) !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.5) !important;
        color: var(--text-color) !important;
    }
    
    .stButton>button {
        background-color: var(--accent-color) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
    }
    
    .stButton>button:hover {
        background-color: #059669 !important; /* Darker Emerald */
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.5) !important;
    }
    
    .stMetric {
        background-color: var(--surface-color) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.5) !important;
        color: var(--text-color) !important;
    }
    
    .stDataFrame {
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.5) !important;
        color: var(--text-color) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-color) !important;
        color: white !important;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1f2937 0%, #4b5563 100%) !important;
        color: white !important;
    }
    
    .sidebar .sidebar-content a {
        color: var(--accent-color) !important;
    }
    
    .sidebar .sidebar-content .stMarkdown h1, 
    .sidebar .sidebar-content .stMarkdown h2,
    .sidebar .sidebar-content .stMarkdown h3 {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Title Section
st.title("🌍 Global Markets Pro")
st.markdown("""
<div style="color: var(--text-secondary); margin-bottom: 2rem;">
    Professional-grade market data analysis for investors and traders
</div>
""", unsafe_allow_html=True)

# Enhanced Ticker List (500+ global companies)
GLOBAL_TICKERS = {
    "Technology": [
        "AAPL", "MSFT", "NVDA", "AVGO", "ASML", "TSM", "ADBE", "CSCO", "ACN", "CRM",
        "ORCL", "SAP", "INTU", "AMD", "INTC", "QCOM", "TXN", "AMAT", "LRCX", "KLAC",
        "SNOW", "PLTR", "U", "DDOG", "ZS", "CRWD", "NET", "MDB", "NOW", "TEAM"
    ],
    "Finance": [
        "JPM", "BAC", "WFC", "C", "HSBC", "GS", "MS", "BLK", "SCHW", "AXP",
        "V", "MA", "PYPL", "SQ", "COIN", "MUFG", "RY", "TD", "BNPQY", "ING"
    ],
    "Consumer": [
        "AMZN", "WMT", "COST", "TGT", "HD", "LOW", "NKE", "MCD", "SBUX", "PEP",
        "KO", "PG", "UL", "NSRGY", "EL", "LVMUY", "KHC", "PM", "MO", "BUD"
    ],
    "Healthcare": [
        "JNJ", "PFE", "ABBV", "LLY", "MRK", "NVS", "AZN", "UNH", "DHR", "TMO",
        "ISRG", "SYK", "BDX", "BSX", "MDT", "ZTS", "VRTX", "REGN", "GILD", "BMY"
    ],
    "Energy & Industrials": [
        "XOM", "CVX", "SHEL", "TTE", "BP", "ENB", "COP", "EOG", "BHP", "RIO",
        "CAT", "DE", "HON", "GE", "BA", "RTX", "LMT", "NOC", "GD", "MMM"
    ],
    "Emerging Markets": [
        "BABA", "TCEHY", "JD", "PDD", "BIDU", "NTES", "TSM", "005930.KS", "000660.KS",
        "0688.HK", "3690.HK", "601318.SS", "600519.SS", "601288.SS", "RELIANCE.NS",
        "TATASTEEL.NS", "INFY", "HDB", "ICICIY", "ITUB"
    ],
    "Crypto & Blockchain": [
        "COIN", "MARA", "RIOT", "MSTR", "HUT", "BITF", "CLSK", "BTBT", "MOGO", "SI"
    ],
    "EV & Clean Energy": [
        "TSLA", "NIO", "LI", "XPEV", "RIVN", "LCID", "FSR", "PLUG", "FCEL", "BE",
        "ENPH", "SEDG", "FSLR", "RUN", "SPWR", "NEE", "DQ", "JKS", "CSIQ"
    ]
}

# Session State Management
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = None
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = None
if 'comparison_tickers' not in st.session_state:
    st.session_state.comparison_tickers = []

# Custom Session with Retries
def create_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    return session

# Enhanced Data Fetching Function
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_stock_data(ticker, start_date, end_date, interval='1d'):
    try:
        ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.history(
            start=start_date,
            end=end_date,
            interval=interval,
            auto_adjust=False,
            actions=True
        )
        if data is None or data.empty:
            return None
        # Calculate technical indicators
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['SMA_200'] = data['Close'].rolling(window=200).mean()
        data['Daily_Return'] = data['Close'].pct_change()
        # Format the data
        data = data.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Adj Close': 'adj_close',
            'Volume': 'volume'
        })
        data = data.reset_index().rename(columns={'Date': 'date'})
        return data[['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 
                    'SMA_50', 'SMA_200', 'Daily_Return']]
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

# Sidebar - Filters and Info
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">Global Markets Pro</h1>
        <p style="color: rgba(255,255,255,0.8);">Professional Market Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sector Selection
    selected_sector = st.selectbox(
        "Select Sector",
        list(GLOBAL_TICKERS.keys()),
        index=0
    )
    
    # Ticker Selection
    selected_ticker = st.selectbox(
        "Select Ticker",
        GLOBAL_TICKERS[selected_sector],
        index=0
    )
    
    # Date Range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=dt.date(2020, 1, 1),
            min_value=dt.date(1980, 1, 1),
            max_value=dt.date.today()
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=dt.date.today(),
            min_value=dt.date(1980, 1, 1),
            max_value=dt.date.today()
        )
    
    # Comparison Tickers
    comparison_tickers = st.multiselect(
        "Compare With (Max 4)",
        [t for sector in GLOBAL_TICKERS.values() for t in sector],
        default=[],
        max_selections=4
    )
    
    # Interval Selection
    interval = st.selectbox(
        "Data Interval",
        ["1d", "1wk", "1mo"],
        index=0
    )
    
    st.markdown("---")
    
    # Social Links
    st.markdown("""
    <div style="margin-top: 2rem;">
        <h3 style="color: white;">Connect</h3>
        <p>
            <a href="mailto:muhammadatiflatif67@gmail.com" style="color: white; text-decoration: none;">
                📧 Email
            </a>
        </p>
        <p>
            <a href="https://www.linkedin.com/in/muhammad-atif-latif-13a171318" style="color: white; text-decoration: none;">
                🔗 LinkedIn
            </a>
        </p>
        <p>
            <a href="https://www.kaggle.com/muhammadatiflatif" style="color: white; text-decoration: none;">
                📊 Kaggle
            </a>
        </p>
        <p>
            <a href="https://x.com/mianatif5867" style="color: white; text-decoration: none;">
                𝕏 Twitter
            </a>
        </p>
        <p>
            <a href="https://github.com/M-Atif-Latif" style="color: white; text-decoration: none;">
                💻 GitHub
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main Content
col1, col2 = st.columns([3, 1])
with col1:
    if st.button("📊 Fetch Market Data", use_container_width=True):
        with st.spinner(f"Loading data for {selected_ticker}..."):
            data = fetch_stock_data(selected_ticker, start_date, end_date, interval)
            if data is not None:
                st.session_state.stock_data = data
                st.session_state.current_ticker = selected_ticker
                st.session_state.comparison_tickers = comparison_tickers
                st.success("Data loaded successfully!")
with col2:
    if st.button("🔄 Clear Data", use_container_width=True, type="secondary"):
        st.session_state.stock_data = None
        st.session_state.current_ticker = None
        st.session_state.comparison_tickers = []
        st.rerun()

# Display Data
if st.session_state.stock_data is not None:
    df = st.session_state.stock_data
    ticker = st.session_state.current_ticker
    
    # Metrics Row
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Current Price",
            f"${df.iloc[-1]['close']:,.2f}",
            f"{df.iloc[-1]['close'] - df.iloc[-2]['close']:,.2f}",
            delta_color="normal"
        )
    with col2:
        st.metric(
            "52 Week Range",
            f"${df['close'].min():,.2f} - ${df['close'].max():,.2f}"
        )
    with col3:
        daily_return = df.iloc[-1]['Daily_Return'] * 100
        st.metric(
            "Daily Return",
            f"{daily_return:.2f}%",
            delta_color="inverse" if daily_return < 0 else "normal"
        )
    with col4:
        vol = df['volume'].mean() / 1_000_000
        st.metric(
            "Avg Volume",
            f"{vol:,.1f}M"
        )
    
    # Interactive Chart
    st.markdown("---")
    st.markdown(f"### {ticker} Price Analysis")
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                       vertical_spacing=0.05, row_heights=[0.7, 0.3])
    
    # Price and Moving Averages
    fig.add_trace(
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name="Price",
            increasing_line_color='#2ecc71',
            decreasing_line_color='#e74c3c'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['SMA_50'],
            name="50-Day SMA",
            line=dict(color='#3498db', width=2)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['SMA_200'],
            name="200-Day SMA",
            line=dict(color='#f39c12', width=2)
        ),
        row=1, col=1
    )
    
    # Volume
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['volume'],
            name="Volume",
            marker_color='#7f8c8d'
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        hovermode="x unified",
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_rangeslider_visible=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Comparison Charts
    if st.session_state.comparison_tickers:
        st.markdown("---")
        st.markdown("### Performance Comparison")
        
        comparison_data = {}
        for comp_ticker in st.session_state.comparison_tickers:
            comp_df = fetch_stock_data(comp_ticker, start_date, end_date, interval)
            if comp_df is not None:
                comparison_data[comp_ticker] = comp_df
        
        if comparison_data:
            fig = go.Figure()
            
            # Normalize all prices to percentage change from start date
            base_price = df.iloc[0]['close']
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=(df['close'] / base_price - 1) * 100,
                    name=ticker,
                    line=dict(width=3)
                )
            )
            
            for comp_ticker, comp_df in comparison_data.items():
                comp_base = comp_df.iloc[0]['close']
                fig.add_trace(
                    go.Scatter(
                        x=comp_df['date'],
                        y=(comp_df['close'] / comp_base - 1) * 100,
                        name=comp_ticker
                    )
                )
            
            fig.update_layout(
                title="Normalized Performance Comparison",
                yaxis_title="Percentage Change (%)",
                hovermode="x unified",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Data Table and Export
    st.markdown("---")
    st.markdown("### Market Data Table")
    
    # Show technical indicators in the table
    display_cols = ['date', 'open', 'high', 'low', 'close', 'volume', 
                   'SMA_50', 'SMA_200', 'Daily_Return']
    
    st.dataframe(
        df[display_cols].rename(columns={
            'date': 'Date',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume',
            'SMA_50': '50-Day SMA',
            'SMA_200': '200-Day SMA',
            'Daily_Return': 'Daily Return'
        }).style.format({
            'Open': '{:,.2f}',
            'High': '{:,.2f}',
            'Low': '{:,.2f}',
            'Close': '{:,.2f}',
            'Volume': '{:,.0f}',
            '50-Day SMA': '{:,.2f}',
            '200-Day SMA': '{:,.2f}',
            'Daily Return': '{:.2%}'
        }),
        height=400,
        use_container_width=True
    )
    
    # Export Options
    st.markdown("---")
    st.markdown("### Export Data")
    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv,
            file_name=f"{ticker}_market_data_{start_date}_to_{end_date}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col2:
        # Export Plotly chart as PNG
        try:
            chart_png = fig.to_image(format="png")
            st.download_button(
                "📊 Download Chart as PNG",
                chart_png,
                file_name=f"{ticker}_chart.png",
                mime="image/png",
                use_container_width=True
            )
        except Exception as e:
            st.download_button(
                "📊 Download Chart as PNG",
                b"",
                file_name=f"{ticker}_chart.png",
                disabled=True,
                help=f"PNG export failed: {str(e)}",
                use_container_width=True
            )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: var(--text-secondary); padding: 1rem;">
    <p>Global Markets Pro • Professional Market Analysis Tool</p>
    <p style="font-size: 0.8rem;">Data provided by Yahoo Finance • Updated at {}</p>
</div>
""".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)

# Global Markets Pro

A professional-grade market data analysis tool for investors and traders, built with Streamlit and yfinance. Visualize, analyze, and export global stock market data with interactive charts and technical indicators.

## Features

- **Modern UI**: Clean, dark-themed interface for a professional look.
- **Global Ticker Coverage**: 500+ tickers across Technology, Finance, Consumer, Healthcare, Energy, Industrials, Emerging Markets, Crypto, and Clean Energy sectors.
- **Custom Date Range & Interval**: Select start/end dates and data interval (daily, weekly, monthly).
- **Technical Indicators**: 50-day and 200-day Simple Moving Averages, daily returns, and more.
- **Interactive Charts**: Candlestick, moving averages, and volume with Plotly.
- **Performance Comparison**: Compare up to 4 tickers on normalized returns.
- **Data Table**: View and export all market data and indicators.
- **Export Options**: Download data as CSV and charts as PNG images.

## Installation

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd yfinnance
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app:
```sh
streamlit run app.py
```

## Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies

## How It Works
- Select a sector and ticker from the sidebar
- Choose date range and interval
- Click **Fetch Market Data** to load and visualize
- Use the export buttons to download data or chart

## Data Source
- Yahoo Finance (via yfinance)
---
*Global Markets Pro • Professional Market Analysis Tool*

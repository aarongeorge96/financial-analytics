# Financial Analytics

A data pipeline that extracts financial market data and loads it into BigQuery for analysis.

## Overview

This project:
1. Extracts stock prices from Alpha Vantage API
2. Extracts economic indicators from FRED API
3. Loads the data into Google BigQuery
4. Analyzes trends using SQL

## Data Sources

**Stock Prices (Alpha Vantage)**
- Daily OHLCV data (Open, High, Low, Close, Volume)
- Tickers: AAPL, MSFT, GOOGL, AMZN, META

**Economic Indicators (FRED)**
- Unemployment Rate (UNRATE)
- Inflation / CPI (CPIAUCSL)
- Federal Funds Rate (FEDFUNDS)

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your API keys

## API Keys Required

- **Alpha Vantage**: Free at https://www.alphavantage.co/support/#api-key
- **FRED**: Free at https://fred.stlouisfed.org/docs/api/api_key.html
- **Google Cloud**: Create a project at https://console.cloud.google.com

## Usage

Extract data:
```bash
python -m financial_analytics.extract
```

Load to BigQuery:
```bash
python -m financial_analytics.load
```

## Project Structure
```
financial-analytics/
├── financial_analytics/   # Python package
│   ├── __init__.py
│   ├── extract.py         # Data extraction from APIs
│   └── load.py            # Load data to BigQuery
├── sql/                   # SQL analysis queries
├── data/                  # Local parquet files
├── tests/                 # Unit tests
├── .env.example           # Environment template
├── .gitignore
├── requirements.txt
└── README.md
```

## Output Files

After running extraction:
- `data/stocks.parquet` — Stock price data
- `data/economic.parquet` — Economic indicator data
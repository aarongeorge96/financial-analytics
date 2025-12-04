"""
Extract financial data from Yahoo Finance and FRED.
"""

import requests
import pandas as pd
from fredapi import Fred
from datetime import datetime
from pathlib import Path
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
FRED_API_KEY = os.getenv("FRED_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
DATA_DIR = Path(__file__).parent.parent / "data"

# Stocks to download
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

# Economic indicators from FRED
FRED_SERIES = {
    "unemployment":"UNRATE",
    "inflation":"CPIAUCSL",
    "fred_rate":"FEDFUNDS",
}

# Date Range
START_DATE = "2020-01-01"

# Extract stock prices
def extract_stock_prices():
    print(f"Extracting stock prices for {len(TICKERS)} tickers...")
    
    all_data = []

    for ticker in TICKERS:
        print(f"{ticker}...", end=" ")
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if "Time Series (Daily)" not in data:
            print(f"Error: {data}")
            time.sleep(12)  # Rate limit is 5 calls per minute
            continue
        
        # Convert to dataframe
        prices = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(prices, orient="index")

        # Clean up
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df = df[df.index >= START_DATE]

        # Rename columns
        df.columns = [col.split(". ")[1] for col in df.columns]
        df = df.astype(float)

        # Add ticker
        df["ticker"] = ticker
        df = df.reset_index()
        df = df.rename(columns={"index":"date"})

        all_data.append(df)
        print(f"{len(df)} rows")

        time.sleep(12)  # Rate limit: 5 calls per minute

    # Combine all dataframes
    combined = pd.concat(all_data, ignore_index=True)

    # Add time stamp
    combined["extracted_at"] = datetime.now()

    print(f"Total {len(combined)} rows")
    return combined

# Download economic indicators from FRED
def extract_economic_data():
    print(f"Downloading {len(FRED_SERIES)} economic indicators...")

    fred = Fred(api_key=FRED_API_KEY)
    all_data = []

    for name, series_id in FRED_SERIES.items():
        print(f"{name}...", end=" ")

        series = fred.get_series(series_id, observation_start=START_DATE)

        df = pd.DataFrame({
            "date": series.index,
            "value": series.values,
            "indicator": name,
        })

        all_data.append(df)
        print(f"{len(df)} rows")

    # Combine all dataframes
    combined = pd.concat(all_data, ignore_index=True)

    # Add time stamp
    combined["extracted_at"] = datetime.now()

    print(f"Total {len(combined)} rows")
    return combined

# Save data frame to parquet file in the data directory
def save_to_parquet(df, filename):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    filepath = DATA_DIR / filename
    df.to_parquet(filepath, index = False)
    
    print(f"Saved: {filepath}")
    return filepath

if __name__ == "__main__":

    #Extract stock prices
    stocks_df = extract_stock_prices()
    save_to_parquet(stocks_df, "stocks.parquet")

    #Extract economic data
    economic_df = extract_economic_data()
    save_to_parquet(economic_df, "economic.parquet")

    print("Extraction complete!")
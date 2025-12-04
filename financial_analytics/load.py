"""
Load data from parquet files into BigQuery.
"""
import pandas as pd
from google.cloud import bigquery
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
DATA_DIR = Path(__file__).parent.parent / "data"
DATASET_NAME = "financial_data"

# Create BigQuery Client
def get_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
    return bigquery.Client(project=PROJECT_ID)

# Create dataset if it doesnt exist
def create_dataset(client):
    dataset_id = f"{PROJECT_ID}.{DATASET_NAME}"

    try:
        client.get_dataset(dataset_id)
        print(f"Dataset {DATASET_NAME} already exists")
    except Exception:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        client.create_dataset(dataset)
        print(f"Created dataset {DATASET_NAME}")

# Load parquet file into BigQuery table
def load_table(client, filename, table_name):
    filepath = DATA_DIR / filename

    if not filepath.exists():
        print(f"File not found: {filepath}")
        return

    # Read raquet file
    df = pd.read_parquet(filepath)
    
    # Create full table ID
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.{table_name}"

    # Load to BigQuery
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result() #Wait for job to be completed

    print(f"Loaded {len(df)} rows into {table_name}")

if __name__ == "__main__":
    client = get_client()

    # Create dataset
    create_dataset(client)

    # Load tables
    load_table(client, "stocks.parquet", "stock_prices")
    load_table(client, "economic.parquet", "economic_indicators")

    print("Load complete!")

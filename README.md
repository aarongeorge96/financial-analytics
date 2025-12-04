\# Financial Analytics



A data pipeline that extracts financial market data and loads it into BigQuery for analysis.



\## Overview



This project:

1\. Extracts stock prices from Yahoo Finance

2\. Extracts economic indicators from FRED

3\. Loads the data into Google BigQuery

4\. Analyzes trends using SQL



\## Setup



1\. Clone the repository

2\. Create a virtual environment: `python -m venv venv`

3\. Activate it: `venv\\Scripts\\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)

4\. Install dependencies: `pip install -r requirements.txt`

5\. Copy `.env.example` to `.env` and fill in your credentials

6\. Set up Google Cloud authentication (see below)



\## Google Cloud Setup



1\. Create a Google Cloud project

2\. Enable the BigQuery API

3\. Create a service account and download the JSON key

4\. Set the path in your `.env` file



\## Usage



Extract data:

```bash

python -m financial\_analytics.extract

```



Load to BigQuery:

```bash

python -m financial\_analytics.load

```



\## Project Structure

```

financial-analytics/

├── financial\_analytics/   # Python package

│   ├── extract.py         # Data extraction scripts

│   └── load.py            # BigQuery loading scripts

├── sql/                   # SQL analysis queries

├── data/                  # Local data files

├── tests/                 # Unit tests

├── .env.example           # Environment template

├── requirements.txt       # Dependencies

└── README.md

```


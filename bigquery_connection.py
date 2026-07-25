from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

# ==========================================
# Google Cloud Project Configuration
# ==========================================

PROJECT_ID = "insightflow-bi-platform"

import streamlit as st

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(
    credentials=credentials,
    project=PROJECT_ID
)

# ==========================================
# BigQuery Table
# ==========================================

QUERY = """
SELECT *
FROM `insightflow-bi-platform.insightflow_dw.sales`
"""

# ==========================================
# Function to Load Data
# ==========================================

def load_data():
    df = client.query(QUERY).to_dataframe()
    return df


# ==========================================
# Test BigQuery Connection
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("Connecting to Google BigQuery...")
    print("=" * 50)

    try:
        df = load_data()

        print("Connection Successful!")
        print(f"Total Rows Loaded : {len(df)}")
        print(f"Total Columns     : {len(df.columns)}")

        print("\nFirst 5 Rows:\n")
        print(df.head())

    except Exception as e:
        print("\nConnection Failed!")
        print(e)
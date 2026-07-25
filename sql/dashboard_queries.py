from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ID = "insightflow-bi-platform"

credentials = service_account.Credentials.from_service_account_file(
    "credentials.json"
)

client = bigquery.Client(
    credentials=credentials,
    project=PROJECT_ID
)

def run_query(query):
    return client.query(query).to_dataframe()
import pandas as pd
import os

# Create processed folder if it doesn't exist
os.makedirs("data/processed", exist_ok=True)

# Load dataset
df = pd.read_excel("data/raw/Sample - Superstore.xls")

# Remove duplicate rows
df = df.drop_duplicates()

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Standardize column names
df.columns = (
    df.columns.str.strip()
              .str.lower()
              .str.replace(" ", "_")
              .str.replace("-", "_")
)

# Remove rows with missing values
df = df.dropna()

# Save cleaned dataset
df.to_csv("data/processed/superstore_clean.csv", index=False)

print("====================================")
print("Cleaning Completed Successfully")
print("Rows :", df.shape[0])
print("Columns :", df.shape[1])
print("====================================")
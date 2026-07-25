import pandas as pd
import matplotlib.pyplot as plt
import os

# Create images folder
os.makedirs("images", exist_ok=True)

# Load cleaned data
df = pd.read_csv("data/processed/superstore_clean.csv")

# ------------------------
# Sales by Category
# ------------------------
sales = df.groupby("category")["sales"].sum()

plt.figure(figsize=(8,5))
sales.plot(kind="bar")
plt.title("Sales by Category")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("images/sales_by_category.png")
plt.close()

# ------------------------
# Profit by Category
# ------------------------
profit = df.groupby("category")["profit"].sum()

plt.figure(figsize=(8,5))
profit.plot(kind="bar")
plt.title("Profit by Category")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig("images/profit_by_category.png")
plt.close()

# ------------------------
# Sales by Region
# ------------------------
region = df.groupby("region")["sales"].sum()

plt.figure(figsize=(8,5))
region.plot(kind="bar")
plt.title("Sales by Region")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("images/sales_by_region.png")
plt.close()

# ------------------------
# Monthly Sales Trend
# ------------------------
df["order_date"] = pd.to_datetime(df["order_date"])

monthly = df.groupby(df["order_date"].dt.to_period("M"))["sales"].sum()

plt.figure(figsize=(12,5))
monthly.plot()
plt.title("Monthly Sales Trend")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("images/monthly_sales.png")
plt.close()

# ------------------------
# Top 10 Customers
# ------------------------
customers = (
    df.groupby("customer_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))
customers.plot(kind="bar")
plt.title("Top 10 Customers")
plt.tight_layout()
plt.savefig("images/top_customers.png")
plt.close()

print("EDA Completed Successfully")
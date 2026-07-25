import streamlit as st
import pandas as pd
import plotly.express as px

# Import BigQuery function
from datetime import datetime
from bigquery_connection import load_data

# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="InsightFlow BI Platform",
    page_icon="📊",
    layout="wide"
)

# ==========================
# Title
# ==========================
st.title("📊 InsightFlow Cloud Business Intelligence Platform")
st.markdown("### Real-time Business Intelligence Dashboard")
st.info(
    "📈 Analyze business performance using interactive dashboards powered by "
    "Python, Streamlit, Plotly, and Google BigQuery."
)
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.caption(
    f"🕒 Last Refreshed: {datetime.now().strftime('%d %b %Y, %I:%M:%S %p')}"
)

# ==========================
# Load Data from BigQuery
# ==========================
@st.cache_data(ttl=600)
def get_data():
    """Load data from BigQuery and cache for 10 minutes."""
    try:
        return load_data()
    except Exception as e:
        st.error("❌ Failed to load data from Google BigQuery.")
        st.exception(e)   # Remove this line before final deployment if you don't want technical details shown.
        return None

df = get_data()

if df is None:
    st.stop()

# ==========================
# Data Cleaning
# ==========================

# Convert column names to lowercase
df.columns = df.columns.str.strip().str.lower()

# Convert Order Date
df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

df = df.dropna(subset=["order_date"])

# ==========================
# Sidebar Filters
# ==========================
st.sidebar.title("📊 InsightFlow")
st.sidebar.markdown("### Dashboard Filters")

selected_region = st.sidebar.multiselect(
    "🌍 Region",
    options=sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

selected_category = st.sidebar.multiselect(
    "📦 Category",
    options=sorted(df["category"].unique()),
    default=sorted(df["category"].unique())
)

selected_segment = st.sidebar.multiselect(
    "👥 Segment",
    options=sorted(df["segment"].unique()),
    default=sorted(df["segment"].unique())
)
st.sidebar.markdown("### 📅 Date Range")

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["order_date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["order_date"].max().date()
)
if start_date > end_date:
    st.sidebar.error("Start Date cannot be after End Date.")
    st.stop()

filtered_df = df[
    (df["region"].isin(selected_region))
    & (df["category"].isin(selected_category))
    & (df["segment"].isin(selected_segment))
    & (df["order_date"] >= pd.to_datetime(start_date))
    & (df["order_date"] <= pd.to_datetime(end_date))
]
if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ Project Information")

st.sidebar.info("""
**InsightFlow Cloud Business Intelligence Platform**

Built with:
- 🐍 Python
- 📊 Streamlit
- ☁️ Google BigQuery
- 📈 Plotly
""")

# ==========================
# KPI Cards
# ==========================
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
total_orders = len(filtered_df)
total_customers = filtered_df["customer_id"].nunique()

# New KPIs
total_quantity = filtered_df["quantity"].sum()

average_order_value = (
    total_sales / total_orders if total_orders > 0 else 0
)

average_discount = filtered_df["discount"].mean()

profit_margin = (
    (total_profit / total_sales) * 100 if total_sales > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("📦 Orders", f"{total_orders:,}")
col4.metric("👥 Customers", f"{total_customers:,}")

col5, col6, col7, col8 = st.columns(4)

col5.metric("📦 Quantity Sold", f"{total_quantity:,}")
col6.metric("🛒 Avg Order Value", f"${average_order_value:,.2f}")
col7.metric("🏷 Avg Discount", f"{average_discount:.2%}")
col8.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

st.divider()

st.markdown("### 📌 Dashboard Summary")

st.success(
    f"""
    • Total Sales: ${total_sales:,.2f}
    • Total Profit: ${total_profit:,.2f}
    • Orders: {total_orders:,}
    • Customers: {total_customers:,}
    • Profit Margin: {profit_margin:.2f}%
    """
)

# ==========================
# Sales by Category
# ==========================
st.subheader("📊 Sales by Category")

category_sales = (
    filtered_df.groupby("category")["sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_sales,
    x="category",
    y="sales",
    color="category",
    title="Sales by Category"
)
fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Profit by Category
# ==========================
st.subheader("💹 Profit by Category")

profit_category = (
    filtered_df.groupby("category")["profit"]
    .sum()
    .reset_index()
)

fig = px.bar(
    profit_category,
    x="category",
    y="profit",
    color="category",
    title="Profit by Category"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Sales by Region
# ==========================
st.subheader("🌍 Sales by Region")

region_sales = (
    filtered_df.groupby("region")["sales"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_sales,
    names="region",
    values="sales",
    title="Sales Distribution by Region"
)
fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Profit by Region
# ==========================
st.subheader("💰 Profit by Region")

profit_region = (
    filtered_df.groupby("region")["profit"]
    .sum()
    .reset_index()
)

fig = px.pie(
    profit_region,
    names="region",
    values="profit",
    title="Profit Distribution by Region"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Sales by Segment
# ==========================
st.subheader("👥 Sales by Segment")

segment_sales = (
    filtered_df.groupby("segment")["sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    segment_sales,
    x="segment",
    y="sales",
    color="segment",
    title="Sales by Customer Segment"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Top 10 States by Sales
# ==========================
st.subheader("🗺️ Top 10 States by Sales")

top_states = (
    filtered_df.groupby("state_province")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_states,
    x="state_province",
    y="sales",
    color="sales",
    title="Top 10 States by Sales"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500,
    xaxis_title="State",
    yaxis_title="Sales"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Monthly Sales Trend
# ==========================
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby(filtered_df["order_date"].dt.to_period("M"))["sales"]
    .sum()
    .reset_index()
)

monthly_sales["order_date"] = monthly_sales["order_date"].astype(str)

fig = px.line(
    monthly_sales,
    x="order_date",
    y="sales",
    markers=True,
    title="Monthly Sales Trend"
)
fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Monthly Profit Trend
# ==========================
st.subheader("📈 Monthly Profit Trend")

monthly_profit = (
    filtered_df.groupby(filtered_df["order_date"].dt.to_period("M"))["profit"]
    .sum()
    .reset_index()
)

monthly_profit["order_date"] = monthly_profit["order_date"].astype(str)

fig = px.line(
    monthly_profit,
    x="order_date",
    y="profit",
    markers=True,
    title="Monthly Profit Trend"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500,
    xaxis_title="Month",
    yaxis_title="Profit"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Sales vs Profit
# ==========================
st.subheader("📊 Sales vs Profit")

sales_profit = (
    filtered_df.groupby("category")[["sales", "profit"]]
    .sum()
    .reset_index()
)

fig = px.scatter(
    sales_profit,
    x="sales",
    y="profit",
    color="category",
    size="sales",
    hover_name="category",
    title="Sales vs Profit by Category"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500,
    xaxis_title="Sales",
    yaxis_title="Profit"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Correlation Heatmap
# ==========================
st.subheader("🔥 Correlation Heatmap")

corr = filtered_df[
    ["sales", "profit", "quantity", "discount"]
].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="Blues",
    title="Correlation Between Business Metrics"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Top Customers
# ==========================
st.subheader("🏆 Top 10 Customers")

top_customers = (
    filtered_df.groupby("customer_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_customers,
    x="customer_name",
    y="sales",
    color="sales",
    title="Top 10 Customers by Sales"
)
fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)
st.plotly_chart(fig, use_container_width=True)

# ==========================
# Top Products
# ==========================
st.subheader("🏆 Top 10 Products")

top_products = (
    filtered_df.groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="product_name",
    y="sales",
    color="sales",
    title="Top 10 Products"
)
fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Business Insights
# ==========================
st.subheader("💡 Business Insights")

top_category = (
    filtered_df.groupby("category")["sales"]
    .sum()
    .idxmax()
)

top_region = (
    filtered_df.groupby("region")["sales"]
    .sum()
    .idxmax()
)

top_segment = (
    filtered_df.groupby("segment")["sales"]
    .sum()
    .idxmax()
)

st.info(
    f"""
    📌 Highest Sales Category: **{top_category}**

    🌍 Best Performing Region: **{top_region}**

    👥 Top Customer Segment: **{top_segment}**
    """
)

# ==========================
# Download Filtered Data
# ==========================
st.subheader("📥 Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv",
)
# ==========================
# Dataset Preview
# ==========================
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head(10), use_container_width=True)
st.divider()

st.caption(
    "InsightFlow Cloud Business Intelligence Platform | "
    "Built with Python, Streamlit, Plotly & Google BigQuery"
)
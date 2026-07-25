from sql.dashboard_queries import run_query

query = """
SELECT
    category,
    SUM(sales) AS total_sales
FROM `insightflow-bi-platform.insightflow_dw.sales`
GROUP BY category
"""

df = run_query(query)

print(df)
import re

sql_query = """
```sql
WITH monthly_revenue AS (
    SELECT 
    
        DATE_TRUNC('month', order_date) AS month, -- Truncate to month
        region,
        SUM((unit_price * units) - discount) AS revenue -- Calculate revenue
    FROM 
        fact_sales
    WHERE 
        EXTRACT(YEAR FROM order_date) = 2024 -- Filter for the year 2024
    GROUP BY 
        month, region
),
total_revenue AS (
    SELECT 
        region,
        SUM(revenue) AS total_revenue -- Sum revenue by region
    FROM 
        monthly_revenue
    GROUP BY 
        region
    ORDER BY 
        total_revenue DESC
    LIMIT 5 -- Get top 5 regions by total revenue
)
SELECT 
    region,
    total_revenue
FROM 
    total_revenue; -- Final selection of top regions
```
"""

# Regex to find single-line comments and replace with an empty string
clean_sql = re.sub(r'--.*$', '', sql_query, flags=re.MULTILINE)

print(clean_sql)
USE EcommerceAnalytics;
GO

CREATE OR ALTER VIEW dbo.vw_monthly_sales AS
SELECT
    YEAR(order_date) AS [year],
    MONTH(order_date) AS [month],
    CONVERT(CHAR(7), order_date, 126) AS year_month,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(quantity) AS units_sold,
    CAST(SUM(quantity * unit_price) AS DECIMAL(12,2)) AS revenue
FROM dbo.order_lines
GROUP BY YEAR(order_date), MONTH(order_date), CONVERT(CHAR(7), order_date, 126);
GO

CREATE OR ALTER VIEW dbo.vw_category_sales AS
SELECT
    category,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(quantity) AS units_sold,
    CAST(SUM(quantity * unit_price) AS DECIMAL(12,2)) AS revenue
FROM dbo.order_lines
GROUP BY category;
GO

CREATE OR ALTER VIEW dbo.vw_regional_sales AS
SELECT
    region,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(quantity) AS units_sold,
    CAST(SUM(quantity * unit_price) AS DECIMAL(12,2)) AS revenue
FROM dbo.order_lines
GROUP BY region;
GO
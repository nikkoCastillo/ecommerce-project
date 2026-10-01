USE EcommerceDemo;
GO

IF OBJECT_ID('dbo.vw_MonthlySales', 'V') IS NOT NULL
    DROP VIEW dbo.vw_MonthlySales;
GO

CREATE VIEW dbo.vw_MonthlySales AS
SELECT
    CAST(DATEADD(month, DATEDIFF(month, 0, o.OrderDate), 0) AS date) AS MonthStart,
    COUNT(DISTINCT o.OrderID) AS OrderCount,
    SUM(oi.Quantity * oi.UnitPrice) AS Revenue
FROM dbo.Orders AS o
INNER JOIN dbo.OrderItems AS oi
    ON oi.OrderID = o.OrderID
WHERE o.Status = N'Completed'
GROUP BY
    DATEADD(month, DATEDIFF(month, 0, o.OrderDate), 0);
GO

SELECT
    MonthStart,
    OrderCount,
    Revenue
FROM dbo.vw_MonthlySales
ORDER BY MonthStart;
GO

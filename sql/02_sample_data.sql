USE EcommerceAnalytics;
GO

IF NOT EXISTS (SELECT 1 FROM dbo.order_lines)
BEGIN
    INSERT INTO dbo.order_lines
        (order_id, order_date, product_name, category, region, quantity, unit_price)
    VALUES
        ('ORD-1001', '2025-01-08', N'Canvas Tote', N'Accessories', N'West', 2, 18.00),
        ('ORD-1001', '2025-01-08', N'Trail Bottle', N'Outdoors', N'West', 1, 24.00),
        ('ORD-1002', '2025-01-19', N'Everyday Tee', N'Clothing', N'East', 3, 22.00),
        ('ORD-1003', '2025-02-03', N'Trail Bottle', N'Outdoors', N'North', 2, 24.00),
        ('ORD-1004', '2025-02-16', N'Canvas Tote', N'Accessories', N'South', 1, 18.00),
        ('ORD-1005', '2025-02-25', N'Everyday Tee', N'Clothing', N'West', 2, 22.00),
        ('ORD-1006', '2025-03-04', N'Field Jacket', N'Clothing', N'East', 1, 89.00),
        ('ORD-1007', '2025-03-12', N'Trail Bottle', N'Outdoors', N'South', 3, 24.00),
        ('ORD-1008', '2025-03-21', N'Canvas Tote', N'Accessories', N'North', 2, 18.00),
        ('ORD-1009', '2025-04-02', N'Field Jacket', N'Clothing', N'West', 2, 89.00),
        ('ORD-1010', '2025-04-11', N'Trail Bottle', N'Outdoors', N'East', 1, 24.00),
        ('ORD-1011', '2025-04-24', N'Everyday Tee', N'Clothing', N'South', 4, 22.00),
        ('ORD-1012', '2025-05-06', N'Canvas Tote', N'Accessories', N'East', 3, 18.00),
        ('ORD-1013', '2025-05-15', N'Field Jacket', N'Clothing', N'North', 1, 89.00),
        ('ORD-1014', '2025-05-27', N'Trail Bottle', N'Outdoors', N'West', 2, 24.00),
        ('ORD-1015', '2025-06-03', N'Everyday Tee', N'Clothing', N'North', 2, 22.00),
        ('ORD-1016', '2025-06-13', N'Canvas Tote', N'Accessories', N'South', 1, 18.00),
        ('ORD-1017', '2025-06-22', N'Field Jacket', N'Clothing', N'East', 1, 89.00);
END;
GO
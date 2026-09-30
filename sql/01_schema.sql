IF DB_ID(N'EcommerceAnalytics') IS NULL
    EXEC(N'CREATE DATABASE EcommerceAnalytics');
GO

USE EcommerceAnalytics;
GO

IF OBJECT_ID(N'dbo.order_lines', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.order_lines
    (
        order_line_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        order_id VARCHAR(20) NOT NULL,
        order_date DATE NOT NULL,
        product_name NVARCHAR(100) NOT NULL,
        category NVARCHAR(50) NOT NULL,
        region NVARCHAR(50) NOT NULL,
        quantity INT NOT NULL CHECK (quantity > 0),
        unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0)
    );
END;
GO
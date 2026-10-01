USE EcommerceDemo;
GO

CREATE TABLE dbo.Users (
    UserID int IDENTITY(1, 1) NOT NULL
        CONSTRAINT PK_Users PRIMARY KEY,
    Email nvarchar(255) NOT NULL
        CONSTRAINT UQ_Users_Email UNIQUE,
    PasswordHash nvarchar(255) NOT NULL,
    IsAdmin bit NOT NULL
        CONSTRAINT DF_Users_IsAdmin DEFAULT (0),
    CreatedAt datetime2 NOT NULL
        CONSTRAINT DF_Users_CreatedAt DEFAULT (SYSUTCDATETIME())
);
GO

CREATE TABLE dbo.Products (
    ProductID int IDENTITY(1, 1) NOT NULL
        CONSTRAINT PK_Products PRIMARY KEY,
    Name nvarchar(120) NOT NULL,
    Category nvarchar(80) NOT NULL,
    Price decimal(10, 2) NOT NULL
        CONSTRAINT CK_Products_Price CHECK (Price >= 0),
    IsActive bit NOT NULL
        CONSTRAINT DF_Products_IsActive DEFAULT (1)
);
GO

CREATE TABLE dbo.Orders (
    OrderID int IDENTITY(1, 1) NOT NULL
        CONSTRAINT PK_Orders PRIMARY KEY,
    UserID int NOT NULL,
    OrderDate datetime2 NOT NULL
        CONSTRAINT DF_Orders_OrderDate DEFAULT (SYSUTCDATETIME()),
    Status nvarchar(20) NOT NULL
        CONSTRAINT DF_Orders_Status DEFAULT (N'Pending'),
    CONSTRAINT FK_Orders_Users
        FOREIGN KEY (UserID) REFERENCES dbo.Users(UserID),
    CONSTRAINT CK_Orders_Status
        CHECK (Status IN (N'Pending', N'Completed', N'Cancelled'))
);
GO

CREATE TABLE dbo.OrderItems (
    OrderItemID int IDENTITY(1, 1) NOT NULL
        CONSTRAINT PK_OrderItems PRIMARY KEY,
    OrderID int NOT NULL,
    ProductID int NOT NULL,
    Quantity int NOT NULL
        CONSTRAINT CK_OrderItems_Quantity CHECK (Quantity > 0),
    UnitPrice decimal(10, 2) NOT NULL
        CONSTRAINT CK_OrderItems_UnitPrice CHECK (UnitPrice >= 0),
    CONSTRAINT FK_OrderItems_Orders
        FOREIGN KEY (OrderID) REFERENCES dbo.Orders(OrderID),
    CONSTRAINT FK_OrderItems_Products
        FOREIGN KEY (ProductID) REFERENCES dbo.Products(ProductID)
);
GO

INSERT INTO dbo.Products (Name, Category, Price) VALUES
    (N'Laptop Stand', N'Accessories', 30.00),
    (N'Wireless Mouse', N'Accessories', 15.00),
    (N'Mechanical Keyboard', N'Accessories', 40.00),
    (N'Ceramic Mug', N'Home', 10.00);
GO
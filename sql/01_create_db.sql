USE master;
GO

IF DB_ID(N'EcommerceDemo') IS NULL
BEGIN
    CREATE DATABASE EcommerceDemo;
END;
GO
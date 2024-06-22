-- Create the database
CREATE DATABASE mob;
GO
USE mob;
GO

-- Create the mobiles table
CREATE TABLE mobiles (
    mobile_id INT PRIMARY KEY IDENTITY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(255) NOT NULL,
    color VARCHAR(50) NOT NULL,
    storage_capacity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    stock_quantity INT NOT NULL,
    CONSTRAINT brand_model_color_unique UNIQUE (brand, model, color)
);

-- Create the discounts table
CREATE TABLE mobile_discounts (
    discount_id INT PRIMARY KEY IDENTITY,
    mobile_id INT NOT NULL,
    pct_discount DECIMAL(5,2) CHECK (pct_discount BETWEEN 0 AND 100),
    FOREIGN KEY (mobile_id) REFERENCES mobiles(mobile_id)
);

-- Create a stored procedure to populate the mobiles table
CREATE PROCEDURE PopulateMobiles
AS
BEGIN
    DECLARE @counter INT = 0;
    DECLARE @max_records INT = 100;
    DECLARE @brand VARCHAR(50);
    DECLARE @model VARCHAR(255);
    DECLARE @color VARCHAR(50);
    DECLARE @storage_capacity INT;
    DECLARE @price DECIMAL(10, 2);
    DECLARE @stock_quantity INT;

    -- Seed the random number generator
    SET @counter = 0;

    WHILE @counter < @max_records
    BEGIN
        -- Generate random values
        SET @brand = (SELECT TOP 1 brand FROM (VALUES ('Apple'), ('Samsung'), ('Google'), ('OnePlus')) AS BrandOptions(brand) ORDER BY NEWID());
        SET @model = CONCAT('Model ', CAST(1 + CAST(RAND() * 10 AS INT) AS VARCHAR(2)));
        SET @color = (SELECT TOP 1 color FROM (VALUES ('Black'), ('White'), ('Silver'), ('Gold')) AS ColorOptions(color) ORDER BY NEWID());
        SET @storage_capacity = CAST(16 + CAST(RAND() * 193 AS INT) AS INT);
        SET @price = CAST(100 + RAND() * 900 AS DECIMAL(10, 2));
        SET @stock_quantity = CAST(10 + RAND() * 91 AS INT);

        -- Attempt to insert a new record
        -- Duplicate brand, model, color combinations will be ignored due to the unique constraint
        BEGIN TRY
            INSERT INTO mobiles (brand, model, color, storage_capacity, price, stock_quantity)
            VALUES (@brand, @model, @color, @storage_capacity, @price, @stock_quantity);
            SET @counter = @counter + 1;
        END TRY
        BEGIN CATCH
            -- Handle duplicate key error
        END CATCH
    END
END;
GO

-- Execute the stored procedure to populate the mobiles table
EXEC PopulateMobiles;
GO

-- Insert at least 10 records into the mobile_discounts table
INSERT INTO mobile_discounts (mobile_id, pct_discount)
VALUES
(1, 10.00),
(2, 15.00),
(3, 20.00),
(4, 5.00),
(5, 25.00),
(6, 10.00),
(7, 30.00),
(8, 35.00),
(9, 40.00),
(10, 45.00);

-- View the contents of the products table
SELECT * FROM mobiles;
GO

-- View the contents of the discounts table
SELECT * FROM mobile_discounts;
GO

SELECT stock_quantity FROM mobiles WHERE brand = 'Apple' AND model = 'Model 4' 
AND color = 'White';

SELECT SUM(stock_quantity) FROM mobiles WHERE brand = 'Samsung';

SELECT color FROM mobiles WHERE model = 'Model 1' AND brand = 'Google' AND color = 'Gold';

SELECT model FROM mobiles WHERE storage_capacity > 128 ORDER BY storage_capacity DESC;

SELECT count(*) FROM mobiles WHERE color = 'White' AND model = 'Model 1';
SELECT stock_quantity FROM mobiles WHERE color = 'White' AND model = 'Model 1';
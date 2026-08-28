
CREATE DATABASE QuickBite;

USE QuickBite;

CREATE TABLE Delivery_performance
(
    order_id VARCHAR(20),
    actual_delivery_time_mins INT,
    expected_delivery_time_mins INT,
    distance_km Decimal,
    delivery_delay INT,
    delivery_status VARCHAR(20)
);

BULK INSERT fact_orders
FROM 'C:\Final Projects\fact orders.csv'
WITH
(
FIRSTROW=2,
FIELDTERMINATOR=',',
ROWTERMINATOR='\n',
TABLOCK
);

Drop table fact_orders

 CREATE TABLE fact_orders
(
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    restaurant_id VARCHAR(20),
    delivery_partner_id VARCHAR(20),
    order_timestamp VARCHAR(25),
    subtotal_amount DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    delivery_fee DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    is_cod CHAR(1),
    is_cancelled CHAR(1),

    order_status_validation VARCHAR(30),
    total_amount_validation VARCHAR(30),
    payment_method VARCHAR(20),
    order_status VARCHAR(20),
    time_slot VARCHAR(20),
    weekday_weekend VARCHAR(20),
    order_phase VARCHAR(20)
);

SELECT TRY_CONVERT(DATETIME, order_timestamp, 105)
FROM fact_orders;

ALTER TABLE fact_orders
ADD order_datetime DATETIME;

UPDATE fact_orders
SET order_datetime =
    CONVERT(DATETIME,
            SUBSTRING(order_timestamp,7,4) + '-' +
            SUBSTRING(order_timestamp,4,2) + '-' +
            SUBSTRING(order_timestamp,1,2) + ' ' +
            SUBSTRING(order_timestamp,12,5));

SELECT TOP 10
order_timestamp,
order_datetime
FROM fact_orders;





CREATE TABLE  Order_items
(
    order_id VARCHAR(20),
    item_id VARCHAR(20),
    menu_item_id VARCHAR(20),
    restaurant_id VARCHAR(20),
    quantity INT,
    unit_price DECIMAL(10,2),
    item_discount DECIMAL(10,2),
    line_total DECIMAL(10,2),
    line_total_validation VARCHAR(20)
);

CREATE TABLE Ratings
(
    order_id VARCHAR(20),
    customer_id VARCHAR(20),
    restaurant_id VARCHAR(20),
    rating INT,
    review_text NVARCHAR(MAX),
    review_timestamp VARCHAR(25),
    sentiment_score DECIMAL(4,2),
    rating_category VARCHAR(10),
    sentiment_category VARCHAR(10),
    month_no TINYINT
);

SELECT TRY_CONVERT(DATETIME, review_timestamp, 105)
FROM  Ratings;


CREATE TABLE Customer
(
    customer_id VARCHAR(20) PRIMARY KEY,
    signup_date VARCHAR(20),
    city VARCHAR(50),
    acquisition_channel VARCHAR(30),
    year INT,
    Month_Name VARCHAR(10),
    customer_age VARCHAR(10)
);

CREATE TABLE Restaurant
(
    restaurant_id VARCHAR(20) PRIMARY KEY,
    restaurant_name VARCHAR(50),
    city VARCHAR(50),
    cuisine_type VARCHAR(50),
    partner_type VARCHAR(30),
    avg_prep_time VARCHAR(20),
    is_active VARCHAR(10),
    preparation_time_strategy VARCHAR(10)
);

CREATE TABLE Delivery_partner
(
    delivery_partner_id VARCHAR(20) PRIMARY KEY,
    partner_name VARCHAR(20),
    city VARCHAR(30),
    vehicle_type VARCHAR(20),
    employment VARCHAR(30),
    avg_rating DECIMAL(3,2),
    is_active VARCHAR(10)
);


CREATE TABLE Menu_item
(
    menu_item_id VARCHAR(20) PRIMARY KEY,
    restaurant_id VARCHAR(20),
    item_name VARCHAR(100),
    category VARCHAR(30),
    is_veg VARCHAR(5),
    price DECIMAL(10,2)
);

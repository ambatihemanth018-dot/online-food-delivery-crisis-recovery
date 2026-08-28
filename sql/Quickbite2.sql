
--- Monthly Orders (Pre-Crisis vs Crisis) ---
--- Problem - How severe is the decline in orders

SELECT
    CASE
        WHEN MONTH(order_datetime) BETWEEN 1 AND 5 THEN 'Pre-Crisis'
        WHEN MONTH(order_datetime) BETWEEN 6 AND 9 THEN 'Crisis'
    END AS Phase,
    MONTH(order_datetime) AS Month,
    COUNT(*) AS Total_Orders
FROM fact_orders
WHERE MONTH(order_datetime) BETWEEN 1 AND 9
GROUP BY
    CASE
        WHEN MONTH(order_datetime) BETWEEN 1 AND 5 THEN 'Pre-Crisis'
        WHEN MONTH(order_datetime) BETWEEN 6 AND 9 THEN 'Crisis'
    END,
    MONTH(order_datetime)
ORDER BY Month;


--- Restaurants Losing Orders ---

SELECT r.restaurant_name,
    CASE
        WHEN MONTH(o.order_datetime) BETWEEN 1 AND 5 THEN 'Pre-Crisis'
        WHEN MONTH(o.order_datetime) BETWEEN 6 AND 9 THEN 'Crisis'
    END AS Phase,
    COUNT(o.order_id) AS Orders
FROM fact_orders o
JOIN Restaurant r
ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_name,
CASE
    WHEN MONTH(o.order_datetime) BETWEEN 1 AND 5 THEN 'Pre-Crisis'
    WHEN MONTH(o.order_datetime) BETWEEN 6 AND 9 THEN 'Crisis'
END
ORDER BY r.restaurant_name;



--- Cancellation Analysis ---

SELECT
      CASE
          WHEN MONTH(order_datetime) BETWEEN 1 AND 5 THEN 'Pre-Crisis'
          WHEN MONTH(order_datetime) BETWEEN 6 AND 9 THEN 'Crisis'
END AS Phase,

COUNT(order_id) AS Orders,
SUM(CASE WHEN is_cancelled='Y' THEN 1 ELSE 0 END) AS Cancelled_Orders,
ROUND(100.0*SUM(CASE WHEN is_cancelled='Y' THEN 1 ELSE 0 END)/COUNT(order_id),2) AS Cancellation_Rate
FROM fact_orders
GROUP BY
CASE
    WHEN MONTH(order_datetime) BETWEEN 1 AND 5 THEN 'Pre-Crisis'
    WHEN MONTH(order_datetime) BETWEEN 6 AND 9 THEN 'Crisis'
END;


--- Ratings Fluctuation ---

SELECT MONTH(o.order_datetime) AS Month,
       ROUND(AVG(r.rating),2) AS Average_Rating
FROM Ratings r
JOIN fact_orders o
ON r.order_id=o.order_id
GROUP BY MONTH(o.order_datetime)
ORDER BY Month;

--- Revenue Impact ---

SELECT
      CASE
          WHEN MONTH(order_datetime) BETWEEN 1 AND 5 THEN 'Pre-Crisis'
          WHEN MONTH(order_datetime) BETWEEN 6 AND 9 THEN 'Crisis'
END AS Phase,
       SUM(subtotal_amount) AS Subtotal,
       SUM(discount_amount) AS Discount,
       SUM(delivery_fee) AS Delivery_Fee,
       SUM(total_amount) AS Revenue
FROM fact_orders
GROUP BY

CASE
     WHEN MONTH(order_datetime) BETWEEN 1 AND 5 THEN 'Pre-Crisis'
     WHEN MONTH(order_datetime) BETWEEN 6 AND 9 THEN 'Crisis'
END;


--- Loyalty Impact ---

SELECT customer_id, COUNT(order_id) AS Orders
FROM fact_orders
WHERE MONTH(order_datetime) BETWEEN 1 AND 5
GROUP BY customer_id
HAVING COUNT(order_id) > =5
ORDER BY Orders DESC;

--- High Value Customers ---

SELECT customer_id,SUM(total_amount) AS Total_Spend,COUNT(order_id) AS Orders
FROM fact_orders
WHERE MONTH(order_datetime) BETWEEN 1 AND 5
GROUP BY customer_id
ORDER BY Total_Spend DESC;


--- Rating vs Delivery Performance ---

SELECT
      CASE
          WHEN actual_delivery_time_mins <= expected_delivery_time_mins
          THEN 'On Time'
          ELSE 'Late'
      END AS Delivery_Status,

COUNT(r.order_id) AS Orders,
ROUND(AVG(r.rating),2) AS Avg_Rating,
ROUND(AVG(r.sentiment_score),2) AS Avg_Sentiment
FROM Ratings r
JOIN Delivery_performance d
ON r.order_id=d.order_id
GROUP BY
        CASE
            WHEN actual_delivery_time_mins <= expected_delivery_time_mins
            THEN 'On Time'
            ELSE 'Late'
END;

--- City-wise Customer Satisfaction ---
--- Which cities have the lowest customer satisfaction

SELECT
    dc.city,
    COUNT(r.order_id) AS Reviews,
    ROUND(AVG(r.Rating),2) AS Avg_Rating,
    ROUND(AVG(r.sentiment_score),2) AS Avg_Sentiment
FROM Ratings r
JOIN customer dc
    ON r.customer_id = dc.customer_id
GROUP BY dc.city
ORDER BY Avg_Rating;


--- Negative review root cause analysis ---

SELECT
    CASE
        WHEN review_text LIKE '%late%' THEN 'Late Delivery'
        WHEN review_text LIKE '%cold%' THEN 'Cold Food'
        WHEN review_text LIKE '%refund%' THEN 'Refund Issue'
        WHEN review_text LIKE '%cancel%' THEN 'Cancellation'
        WHEN review_text LIKE '%missing%' THEN 'Missing Items'
        ELSE 'Other'
    END AS Complaint_Type,
    COUNT(*) AS Total_Complaints
FROM Ratings
WHERE rating <=2
GROUP BY
CASE
        WHEN review_text LIKE '%late%' THEN 'Late Delivery'
        WHEN review_text LIKE '%cold%' THEN 'Cold Food'
        WHEN review_text LIKE '%refund%' THEN 'Refund Issue'
        WHEN review_text LIKE '%cancel%' THEN 'Cancellation'
        WHEN review_text LIKE '%missing%' THEN 'Missing Items'
        ELSE 'Other'
END
ORDER BY Total_Complaints DESC;

🍔 Providing Insights for Crisis Recovery in an Online Food Delivery Startup

📌 Project Overview

An online food delivery startup, QuickBite, experienced a significant business crisis affecting order volume, revenue, customer satisfaction, and retention.

This project uses SQL and Python to investigate the crisis, identify root causes, analyze customer retention, and provide recovery recommendations.

🎯 Business Problem

The startup experienced:

- Declining orders
- Revenue loss
- Increased cancellations
- Rating fluctuations
- Delivery performance issues
- Reduced customer loyalty
- Customer retention decline

The objective is to understand:

1. How severe was the crisis?
2. Which areas of the business were most affected?
3. What caused customer dissatisfaction?
4. Did customers stop returning?
5. How can lost customers be recovered?

🧰 Tools & Technologies
Tool	      Purpose
SQL	      Business analysis, aggregations, customer and restaurant analysis
Python	      Data cleaning, operational analysis, cohort analysis
Pandas	      Data transformation and analysis
NumPy	      Numerical operations
Matplotlib    Data visualization
GitHub	      Version control and project documentation

🗂️ Dataset

The project uses multiple datasets related to:

- Orders
- Order items
- Customer ratings
- Customers
- Restaurants
- Menu items
- Delivery performance

🔄 Project Workflow

```text
Raw Data
   ↓
Data Cleaning & Preparation
   ↓
SQL Business Analysis
   ↓
Python Operational Analysis
   ↓
Customer Retention & Cohort Analysis
   ↓
Root Cause Analysis
   ↓
Recovery Recommendations
                
🗄️ SQL Analysis

1. Monthly Orders: Pre-Crisis vs Crisis

Business Question: How severe was the decline in customer orders?

The analysis compares monthly order volume before and during the crisis.

2. Restaurants Losing Orders

Business Question: Which restaurants experienced the largest decline in orders?

The analysis identifies restaurant partners affected by the crisis.

3. Cancellation Analysis

Business Question: Did cancellations increase during the crisis?

The analysis investigates cancellation trends and identifies areas with higher cancellation rates.

4. Ratings Fluctuation

Business Question: Did customer satisfaction decline during the crisis?

Customer ratings were compared across different periods.

5. Revenue Impact

Business Question: How significantly did the crisis affect revenue?

The analysis measures:

Monthly revenue
Revenue decline
Average order value
Restaurants contributing to revenue loss
6. Loyalty Impact

Business Question: Did existing customers reduce their ordering behavior?

The analysis evaluates repeat customers and changes in customer ordering frequency.

7. High-Value Customers

Business Question: Did QuickBite lose engagement from its most valuable customers?

Customers were analyzed based on:

Total spending
Order frequency
Repeat purchases
Crisis-period activity
8. Rating vs Delivery Performance

Business Question: Did poor delivery performance contribute to lower customer ratings?

The analysis compares expected delivery time, actual delivery time, delivery delays, and customer ratings.

9. City-Wise Customer Satisfaction

Business Question: Which cities experienced the largest decline in customer satisfaction?

Customer ratings and satisfaction trends were compared across cities.

10. Negative Review Root Cause Analysis

Business Question: What caused negative customer experiences?

The analysis investigates potential causes such as:

Late delivery
Food quality
Order accuracy
Preparation delays
Customer service issues

🐍 Python Analysis

Data Preparation 
The data was cleaned and prepared using Python.

Key tasks included:

Missing value checks
Duplicate checks
Data type validation
Timestamp conversion
Order validation
Feature engineering
Key Features Created
Order Status
Payment Method
Time Slot
Weekday / Weekend
Order Phase
Order Month
Delivery Delay Minutes
Late Delivery
Cohort Month
Cohort Index

🚚 Operational Analysis

The analysis investigated:
Actual vs expected delivery time
Delivery delays
Late delivery rate
Distance impact
Restaurant preparation time

Business Question:
Did operational problems contribute to poor customer experience and reduced retention?

👥 Customer Analysis

Customer analysis was conducted to understand customer behavior, loyalty, and identify customers to prioritize for recovery.

## Key Analysis

- **Customer Base:** Total unique customers.
- **One-Time vs Repeat Customers:** Measures customer loyalty and repeat purchase behavior.
- **Acquisition Channels:** Identifies channels generating the most customers and revenue.
- **Customer Distribution:** Analyzes customer concentration across cities.
- **Purchase Behavior:** Measures average order frequency per customer.
- **Customer Value:** Identifies high-value customers based on total spending.

## RFM Customer Segmentation
Customers were segmented using:

- **Recency:** How recently a customer ordered.
- **Frequency:** How often a customer ordered.
- **Monetary:** Total customer spending.

Customer segments include:
- **Champions**
- **Loyal Customers**
- **Potential Loyalists**
- **At-Risk Customers**
- **Lost Customers**

## 🎯 Business Value

This analysis helps QuickBite prioritize high-value and at-risk customers for targeted retention and recovery strategies instead of applying the same incentives to all customers.

👥 Customer Retention & Cohort Analysis
Cohort analysis was used to understand whether customers continued ordering after their first completed purchase.

Customers were grouped based on their first completed order month and their future ordering behavior was tracked.

📉 Key Findings

      Metric	                 Result
Pre-Crisis Retention	         8.92%
Crisis Retention	         3.63%
Retention Decline	         5.28 percentage points
Relative Retention Decline	 59.26%

Key Insight
Customers acquired during the crisis were significantly less likely to return.

This indicates that the recovery challenge is not only acquiring new customers but rebuilding trust and encouraging existing and lapsed customers to return.

🔍 Core Problem Identified

The analysis suggests the following potential business chain:

Operational / Restaurant Issues
             ↓
Poor Customer Experience
             ↓
Negative Ratings & Reviews
             ↓
Cancellations
             ↓
Lower Repeat Orders
             ↓
Customer Retention Decline
             ↓
Revenue Loss

💡 Business Recommendations

1. Prioritize High-Value Lapsed Customers

Identify customers who were previously:    
High spenders
Frequent customers
Loyal customers

Provide targeted recovery incentives instead of generic discounts.


2. Target At-Risk Customer Cohorts

Focus on customer cohorts with:
Low Month-2 retention
High cancellation exposure
Significant decline in repeat orders

Possible strategies:
Personalized offers
Free delivery
Cashback
Re-engagement campaigns


3. Improve Operations Before Increasing Acquisition Spend

The recommended approach is:
Fix Service Problems
        ↓
Improve Customer Experience
        ↓
Improve Customer Retention
        ↓
Scale Customer Acquisition


4. Restaurant-Level Intervention

Prioritize restaurants with:
Declining orders
High cancellations
Low ratings
Long preparation times

Potential interventions include operational reviews and performance monitoring.


🔬 Future Analysis & Recovery Opportunities

The following questions require additional data or experimentation.

Competitor Benchmarking:
Compare QuickBite's performance with competitors to determine whether the decline was company-specific or industry-wide.

CAC Investigation:
Analyze marketing spend, advertising costs, conversion rates, and customer acquisition trends.

A/B Testing Recovery Strategies:
Test different recovery incentives:

Group	       Strategy
Control	       No incentive
A	       Discount
B	       Free Delivery
C	       Cashback

Measure:
Return rate
Repeat order rate
Revenue
Retention
Lapsed Customer Recovery

Prioritize lapsed customers based on:
Previous spending
Order frequency
Recency
Historical loyalty
Cancellation exposure


📊 Key Performance Indicators
     KPI	                               Purpose
Retention Rate	                        Measure customer return
Repeat Order Rate	                Measure loyalty
Cancellation Rate	                Monitor service issues
Late Delivery Rate	                Monitor operations
Average Rating	                        Measure customer satisfaction
Lapsed Customer Reactivation Rate	Measure recovery success
Revenue Recovery	                Measure business improvement


📁 Project Structure
online-food-delivery-crisis-recovery/
│
├── README.md
├── requirements.txt
│
├── data/
│
├── sql/
│   ├── 01_monthly_orders.sql
│   ├── 02_restaurant_order_decline.sql
│   ├── 03_cancellation_analysis.sql
│   ├── 04_ratings_fluctuation.sql
│   ├── 05_revenue_impact.sql
│   ├── 06_loyalty_impact.sql
│   ├── 07_high_value_customers.sql
│   ├── 08_rating_vs_delivery.sql
│   ├── 09_city_customer_satisfaction.sql
│   └── 10_negative_review_root_cause.sql
│
├── python/
│   ├── 01_data_preparation.py
│   ├── 02_crisis_assessment and business_impact_analysis.py
│   ├── 03_operational_diagnosis.py
|   ├── 04_Customer Analysis.pu
│   └── 05_customer_retention_cohort_analysis.py
│
└── visuals/
    ├── monthly_orders.png
    ├── cancellation_analysis.png
    ├── delivery_performance.png
    ├── cohort_heatmap.png
    └── retention_comparison.png
💼 Skills Demonstrated

SQL
Python
Pandas
NumPy
Matplotlib
Data Cleaning
Exploratory Data Analysis
Business Analysis
Customer Behavior Analysis
Operational Analysis
Revenue Analysis
Cohort Analysis
Customer Retention Analysis
Root Cause Analysis
Data Storytelling

🚀 Future Enhancements
Customer segmentation
Lapsed customer return prediction
Churn risk analysis
Sentiment analysis
A/B testing
Customer Lifetime Value analysis
Interactive dashboard

👤 Author
Hemanth Nath
Aspiring Data Analyst
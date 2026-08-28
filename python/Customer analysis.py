
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

orders = pd.read_csv("../data/fact_orders.csv")
customers = pd.read_csv("../data/dim_customer.csv")

### Date converstion ###

orders['order_timestamp'] = pd.to_datetime(orders['order_timestamp'],format='%d-%m-%Y %H:%M')
customers['signup_date'] = pd.to_datetime(customers['signup_date'],format='%d-%m-%Y')

### Merging customer table ###

customer_orders = pd.merge(orders,customers,on='customer_id',how='left')
customer_orders.head()

############## Customer Base Overview ##############

# Total Customers 
total_customers = customer_orders['customer_id'].nunique()
print("Total Customers:", total_customers)


############## New vs Repeat Customers ##############

# One-Time vs Repeat Customers ###
customer_order_counts = ( customer_orders.groupby('customer_id')['order_id'].count())

one_time_customers = customer_order_counts.eq(1).sum()
repeat_customers = customer_order_counts.gt(1).sum()
repeat_rate = ( repeat_customers / total_customers ) * 100

print("One-Time Customers:", one_time_customers)
print("Repeat Customers:", repeat_customers)
print("Repeat Customer Rate:", round(repeat_rate, 2), "%")


############## Customer Acquisition Channel ##############
acquisition = (customer_orders.groupby('acquisition_channel')['customer_id'].nunique().sort_values(ascending=False))
print(acquisition)

acquisition.plot(kind='bar')

plt.title("Customers by Acquisition Channel")
plt.xlabel("Channel")
plt.ylabel("Customers")
plt.show()

### Customers by City ###
city_customers = (customer_orders.groupby('city')['customer_id'].nunique().sort_values(ascending=False))
print(city_customers)

city_customers.plot(kind='bar')

plt.title("Customers by City")
plt.ylabel("Customers")
plt.show()

### Revenue by Acquisition Channel ###
channel_revenue = (customer_orders.groupby('acquisition_channel')['total_amount'].sum().sort_values(ascending=False))
print(channel_revenue)

channel_revenue.plot(kind='bar')

plt.title("Revenue by Acquisition Channel")
plt.xlabel("Acquisition Channel")
plt.ylabel("Revenue")
plt.show()

# Summary 

channel_analysis = (customer_orders.groupby('acquisition_channel').agg(Customers=('customer_id', 'nunique'),Orders=('order_id', 'count'),Revenue=('total_amount', 'sum')))
channel_analysis['Revenue_Per_Customer'] = (channel_analysis['Revenue'] / channel_analysis['Customers'])
print(channel_analysis.sort_values('Revenue_Per_Customer',ascending=False))

############## Customer Purchase Behavior ##############

### Average Orders per Customer ###
orders_per_customer = (customer_orders.groupby('customer_id')['order_id'].count())
print(orders_per_customer.describe())

print("Average Orders Per Customer:",round(orders_per_customer.mean(), 2))
print("Median Orders Per Customer:",round(orders_per_customer.median(), 2))
print("Maximum Orders:",orders_per_customer.max())

############## Customer Value Analysis ##############

clv = (customer_orders.groupby('customer_id')['total_amount'].sum())
print(clv.describe())

customer_value = (customer_orders.groupby('customer_id')['total_amount'].sum())
print(customer_value.describe())

high_value_threshold = customer_value.quantile(0.75)
high_value_customers = customer_value[customer_value >= high_value_threshold]
print("High-Value Customers:",high_value_customers.count())


############## RFM Analysis ############## 

snapshot_date = (customer_orders['order_timestamp'].max() + pd.Timedelta(days=1))
rfm = (customer_orders.groupby('customer_id').agg(
Recency=('order_timestamp',lambda x: (snapshot_date - x.max()).days),
Frequency=('order_id', 'count'),
Monetary=('total_amount', 'sum')).reset_index())

print(rfm.head())
print(rfm.describe())

# RFM Scoring 

rfm['R_Score'] = pd.qcut(rfm['Recency'],5,labels=[5, 4, 3, 2, 1],duplicates='drop')
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'),5,labels=[1, 2, 3, 4, 5],duplicates='drop')
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'),5,labels=[1, 2, 3, 4, 5],duplicates='drop')

# RFM Customer Segmentation

conditions = [

    # Champions
    (rfm['R_Score'].astype(int) >= 4) &
    (rfm['F_Score'].astype(int) >= 4),

    # Loyal Customers
    (rfm['R_Score'].astype(int) >= 3) &
    (rfm['F_Score'].astype(int) >= 3),

    # At Risk
    (rfm['R_Score'].astype(int) <= 2) &
    (rfm['F_Score'].astype(int) >= 3),

    # Lost Customers
    (rfm['R_Score'].astype(int) <= 2) &
    (rfm['F_Score'].astype(int) <= 2)
]

choices = ["Champions","Loyal Customers","At Risk","Lost Customers"]
rfm['Customer_Segment'] = np.select(conditions,choices,default="Potential Loyalists")

segment_count = ( rfm['Customer_Segment'].value_counts())
print(segment_count)

segment_count.plot(kind='bar')

plt.title("Customer Segments")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.show()

# Revenue by Customer Segment 

segment_revenue = (rfm.groupby('Customer_Segment')['Monetary'].mean().sort_values(ascending=False))
print(segment_revenue)

average_customer_value = (rfm.groupby('Customer_Segment')['Monetary'].mean().sort_values(ascending=False))
print(average_customer_value)

average_customer_value.plot(kind='bar')

plt.title("Average Customer Value by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Average Customer Revenue")
plt.show()


segment_summary = (rfm.groupby('Customer_Segment').agg
   (
        Customers=('customer_id', 'count'),
        Total_Revenue=('Monetary', 'sum'),
        Average_Customer_Value=('Monetary', 'mean'),
        Average_Order_Frequency=('Frequency', 'mean')
    )
    .sort_values('Total_Revenue', ascending=False))

print(segment_summary)



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ── LOAD ALL TABLES ─────────────────────────────────────

orders = pd.read_csv(r"C:\Final Projects\fact orders.csv")
Restaurant = pd.read_csv(r"C:\Final Projects\Restaurants.csv")
delivery = pd.read_csv(r"C:\Final Projects\Delivery performance.csv")

# Date conversion:

orders['order_timestamp'] = pd.to_datetime(orders['order_timestamp'],format='%d-%m-%Y %H:%M')

# Delivery performance: 

delivery['Delivery_Delay_Minutes'] = (delivery['actual_delivery_time_mins'] - delivery['expected_delivery_time_mins'])
delivery['Late_Delivery'] = np.where(delivery['Delivery_Delay_Minutes'] > 0,1,0)
print("\nDELIVERY DELAY VERIFICATION")
print(delivery[['actual_delivery_time_mins','expected_delivery_time_mins','Delivery_Delay_Minutes','Late_Delivery']].head())


orders_delivery = orders.merge( delivery,on='order_id',how='left')
missing_delivery = orders_delivery['Delivery_Delay_Minutes'].isna().sum()
print(f"\nMissing delivery records: {missing_delivery}")

# Did delivery performance deteriorate during the crisis:

delivery_phase = (orders_delivery.groupby('Order phase').agg(Avg_Delivery_Delay=('Delivery_Delay_Minutes','mean'),Late_Delivery_Rate=('Late_Delivery','mean')))
delivery_phase['Late_Delivery_Rate'] *= 100
print("\nDELIVERY PERFORMANCE: PRE-CRISIS VS CRISIS")
print(delivery_phase.round(2))

# late deliveries associated with higher cancellations
orders_delivery['Cancelled_Flag'] = np.where(orders_delivery['Order Status'] == 'Cancelled',1,0)

# Are late deliveries associated with higher cancellations:
cancellation_by_delivery = (orders_delivery.groupby('Late_Delivery').agg(Orders=('order_id', 'nunique'),Cancellation_Rate=('Cancelled_Flag','mean')))
cancellation_by_delivery['Cancellation_Rate'] *= 100
cancellation_by_delivery.index = (cancellation_by_delivery.index.map({0: 'On-Time',1: 'Late'}))
print("\nCANCELLATION RATE BY DELIVERY STATUS")
print(cancellation_by_delivery.round(2))

# restaurant preparation time contribute to delivery problems
restaurant_prep = Restaurant[['restaurant_id','avg_prep_time_min','Preparation time category']].drop_duplicates('restaurant_id')
orders_delivery = orders_delivery.merge(restaurant_prep,on='restaurant_id', how='left')
print("\nPREPARATION TIME MERGE")
print(orders_delivery[['restaurant_id','avg_prep_time_min','Preparation time category','Delivery_Delay_Minutes']].head())

# Does restaurant preparation time explain delivery issues:
prep_performance = (orders_delivery.groupby('Preparation time category').agg(Orders=('order_id', 'nunique'),
Avg_Delivery_Delay=('Delivery_Delay_Minutes','mean'),
Late_Delivery_Rate = ('Late_Delivery','mean')))
prep_performance['Late_Delivery_Rate'] *= 100

print("\nPREPARATION TIME PERFORMANCE")
print(prep_performance.round(2))

# Which restaurants should be prioritized:
operational_priority = (orders_delivery.groupby('restaurant_id').agg(Orders=('order_id', 'nunique'),
Avg_Delivery_Delay=('Delivery_Delay_Minutes','mean'),
Late_Delivery_Rate = ('Late_Delivery','mean'),
Cancellation_Rate = ('Cancelled_Flag','mean')))

operational_priority['Late_Delivery_Rate'] *= 100
operational_priority['Cancellation_Rate'] *= 100

# Remove low-volume restaurants
operational_priority = operational_priority[operational_priority['Orders'] >= 20].copy()

# Define performance thresholds
delay_threshold = (operational_priority['Avg_Delivery_Delay'].median())
cancellation_threshold = (operational_priority['Cancellation_Rate'].median())

# Identify priority restaurants
operational_priority['Priority'] = np.where((operational_priority['Avg_Delivery_Delay'] > delay_threshold) 
                                   & (operational_priority['Cancellation_Rate'] > cancellation_threshold),'High Priority','Monitor')
operational_priority = (operational_priority.sort_values(['Priority','Cancellation_Rate'],ascending=[True,False]))
print("\nOPERATIONAL PRIORITY RESTAURANTS")
print(operational_priority[operational_priority['Priority'] == 'High Priority'].head(10).round(2))

# Create OrderMonth
orders_delivery['OrderMonth'] = (orders_delivery['order_timestamp'].dt.to_period('M'))

# Monthly delivery trend
monthly_delivery = (orders_delivery.groupby('OrderMonth')['Delivery_Delay_Minutes'].mean())
plt.figure(figsize=(10, 5))

monthly_delivery.plot(kind='line',marker='o')

plt.title('Monthly Average Delivery Delay')
plt.xlabel('Month')
plt.ylabel('Average Delay (Minutes)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Final summary section
print("\n" + "=" * 60)
print("OPERATIONAL DIAGNOSIS SUMMARY")
print("=" * 60)

print("\n1. Delivery Performance by Phase:")
print(delivery_phase.round(2))

print("\n2. Cancellation Rate by Delivery Status:")
print(cancellation_by_delivery.round(2))

print("\n3. Performance by Preparation Time:")
print(prep_performance.round(2))

print("\n4. Priority Operational Segments:")
print(operational_priority.query("Priority == 'High Priority'").head(10).round(2))
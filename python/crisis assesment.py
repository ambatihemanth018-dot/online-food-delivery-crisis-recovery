
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ── LOAD ALL TABLES ─────────────────────────────────────

orders = pd.read_csv(r"C:\Final Projects\fact orders.csv")
Restaurant = pd.read_csv(r"C:\Final Projects\Restaurants.csv")

orders['order_timestamp'] = pd.to_datetime(orders['order_timestamp'],format='%d-%m-%Y %H:%M',errors='coerce')
orders['OrderMonth'] = (orders['order_timestamp'].dt.to_period('M'))

## KPI calculation 

crisis_kpi = (orders.groupby('Order phase').agg(Orders=('order_id', 'nunique'),
Revenue=('total_amount','sum'),
Active_Customers=('customer_id','nunique'),
Cancellation_Rate=('Order Status',lambda x: (x == 'Cancelled').mean() * 100)))
print("\nCRISIS ASSESSMENT")
print(crisis_kpi.round(2))

## Monthly crisis trend
monthly_trend = (orders.groupby('OrderMonth').agg(Orders=('order_id', 'nunique'),Revenue=('total_amount', 'sum')))
print("\nMONTHLY TREND")
print(monthly_trend)

monthly_trend['Orders'].plot(kind='line',marker='o')
plt.title('Monthly Order Trend')
plt.ylabel('Orders')
plt.tight_layout()
plt.show()


########################## BUSINESS IMPACT CONCENTRATED ######################

## cities experienced the largest decline
# Merge city:
orders_city = orders.merge(Restaurant[['restaurant_id', 'city']].drop_duplicates('restaurant_id'),on='restaurant_id',how='left')
city_impact = ( orders_city[orders_city['Order Status'] == 'Completed'].groupby(['city', 'Order phase'])['order_id'].nunique().unstack())

# Percentage decline:
city_impact['Change_%'] = (( city_impact['Crisis'] - city_impact['Pre-Crisis']) / city_impact['Pre-Crisis']) * 100
print("\nCITY IMPACT")
print(city_impact.sort_values('Change_%'))

# Restaurant partners contributed most to the business decline?
restaurant_impact = ( orders[orders['Order Status'] == 'Completed'].groupby(['restaurant_id', 'Order phase'])['order_id'].nunique().unstack())
restaurant_impact['Order_Change_%'] = (( restaurant_impact['Crisis'] - restaurant_impact['Pre-Crisis']) / restaurant_impact['Pre-Crisis']) * 100
print("\nRESTAURANT IMPACT")
print(restaurant_impact.sort_values('Order_Change_%' ).head(10))




import pandas as pd
import numpy as np
from pathlib import Path
import os
import matplotlib.pyplot as plt


# ── LOAD ALL TABLES ─────────────────────────────────────

orders = pd.read_csv(r"C:\Final Projects\fact orders.csv")
customer = pd.read_csv(r"C:\Final Projects\customer.csv")
Restaurant = pd.read_csv(r"C:\Final Projects\Restaurants.csv")
order_items = pd.read_csv(r"C:\Final Projects\order items.csv")
delivery = pd.read_csv(r"C:\Final Projects\Delivery performance.csv")
delivery_partner = pd.read_csv(r"C:\Final Projects\Delivery partner.csv")
ratings = pd.read_csv(r"C:\Final Projects\Ratings_1.csv")
menu_items = pd.read_csv(r"C:\Final Projects\menu items.csv")


# structure 

""" datasets = {
    "Orders": orders,
    "Customers": customer,
    "Restaurants": Restaurant,
    "Order Items": order_items,
    "Ratings": ratings,
    "Delivery": delivery
}

for name, df in datasets.items():
    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)
    print("Shape:", df.shape)
    print(df.dtypes) """

## Data Conversion

orders['order_timestamp'] = pd.to_datetime(orders['order_timestamp'],format='%d-%m-%Y %H:%M',errors='coerce')
print("\nInvalid order timestamps:",orders['order_timestamp'].isna().sum())

## Remove duplicates
print("Duplicate orders:",orders.duplicated().sum())
orders = orders.drop_duplicates()
orders = orders.drop_duplicates(subset='order_id')

## 0rder status
orders['Order Status'] = np.where(orders['is_cancelled'].str.upper() == 'Y','Cancelled','Completed')
print("\nOrder Status:")
print(orders['Order Status'].value_counts())

## Payment method
orders['Payment Method'] = np.where(orders['is_cod'].str.upper() == 'Y','COD','Online')
print("\nPayment Method:")
print(orders['Payment Method'].value_counts())

# Create business time features
orders['OrderMonth'] = (orders['order_timestamp'].dt.to_period('M'))
orders['Order Phase'] = np.where(orders['OrderMonth'] < pd.Period('2025-06',freq='M'),'Pre-Crisis','Crisis')

# Verification:
print("\nOrder Phase:")
print(orders['Order Phase'].value_counts())

## Create clean analysis dataset
orders_clean = orders.copy()

# ==========================================
# CREATE OUTPUT FOLDER AND SAVE CLEAN DATA
# ==========================================

# Get the folder where this Python script is located
BASE_DIR = Path(__file__).resolve().parent

# Create output folder inside the script folder
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# Final output file path
OUTPUT_FILE = OUTPUT_DIR / "orders_clean.csv"

# Save cleaned dataset
orders_clean.to_csv(OUTPUT_FILE,index=False)
print(f"\nCleaned data saved successfully to:\n{OUTPUT_FILE}")



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ── LOAD ALL TABLES ─────────────────────────────────────
orders = pd.read_csv(r"C:\Final Projects\fact orders.csv")
orders['order_timestamp'] = pd.to_datetime(orders['order_timestamp'],errors='coerce')

# Fliter completed orders
cohort_orders = orders[orders['Order Status'] == 'Completed'].copy()
print("Total orders:", orders.shape[0])
print("Completed orders:", cohort_orders.shape[0])
print("Unique customers:", cohort_orders['customer_id'].nunique())

# Order month
cohort_orders['OrderMonth'] = (cohort_orders['order_timestamp'].dt.to_period('M'))
print(cohort_orders[['order_timestamp', 'OrderMonth']].head())

# Cohort Month
cohort_orders['CohortMonth'] = (cohort_orders.groupby('customer_id')['OrderMonth'].transform('min'))
print(cohort_orders[['customer_id','OrderMonth','CohortMonth']].head(10))

# Cohort index
cohort_orders['CohortIndex'] = ((cohort_orders['OrderMonth'].dt.year - cohort_orders['CohortMonth'].dt.year) * 12
                                       +
    (cohort_orders['OrderMonth'].dt.month - cohort_orders['CohortMonth'].dt.month) + 1)
print(cohort_orders[['customer_id','OrderMonth','CohortMonth','CohortIndex']].head(15))

# ==========================================
#     CUSTOMER COHORT RETENTION
# ==========================================

# Count unique customers from each acquisition cohort
# who returned in subsequent months
cohort_data = (cohort_orders.groupby(['CohortMonth', 'CohortIndex'])['customer_id'].nunique().reset_index())

# cohort matrix
cohort_matrix = (cohort_data.pivot(index='CohortMonth',columns='CohortIndex',values='customer_id'))

# Retention percentages
cohort_size = cohort_matrix[1]
retention_matrix = (cohort_matrix.divide(cohort_size, axis=0) * 100)
print("\nRETENTION MATRIX (%)")
print(retention_matrix.round(2))

# Retention Heatmap
plt.figure(figsize=(12, 7))

plt.imshow(retention_matrix,aspect='auto')
plt.colorbar(label='Retention Rate (%)')
plt.title('Customer Cohort Retention')
plt.xlabel('Months Since First Completed Order')
plt.ylabel('Customer Acquisition Cohort')
plt.xticks(range(len(retention_matrix.columns)),retention_matrix.columns)
plt.yticks(range(len(retention_matrix.index)),retention_matrix.index.astype(str))
plt.tight_layout()
plt.show()

# Did retention decline during the crisis
# ==========================================
#   PRE-CRISIS VS CRISIS RETENTION
# ==========================================

month2_analysis = (retention_matrix.reset_index()[['CohortMonth', 2]].rename(columns={2: 'Month2_Retention'}).dropna())

# Classify acquisition cohorts by phase
month2_analysis['Phase'] = np.where(month2_analysis['CohortMonth'] < pd.Period('2025-06', freq='M'),'Pre-Crisis','Crisis')

# Compare average Month-2 retention
retention_comparison = (month2_analysis.groupby('Phase')['Month2_Retention'].mean())
print("\nPRE-CRISIS VS CRISIS RETENTION")
print(retention_comparison.round(2))

# Quantify the retention impact

# ==========================================
# RETENTION IMPACT
# ==========================================

pre_crisis = retention_comparison.get('Pre-Crisis', np.nan)
crisis = retention_comparison.get('Crisis', np.nan)
retention_decline = pre_crisis - crisis
relative_decline = ( retention_decline / pre_crisis) * 100

print("\nRETENTION IMPACT")
print(f"Pre-Crisis retention: {pre_crisis:.2f}%")
print(f"Crisis retention: {crisis:.2f}%")
print(f"Retention decline: "f"{retention_decline:.2f} percentage points")
print(f"Relative retention decline: "f"{relative_decline:.2f}%")

# Cohorts at risk - Which customer acquisition cohorts should the business prioritize for recovery

# ==========================================
#   COHORTS AT RISK
# ==========================================

cohorts_at_risk = (month2_analysis.sort_values('Month2_Retention',ascending=True))
print("\nTOP 5 CUSTOMER COHORTS AT RISK")
print(cohorts_at_risk[['CohortMonth', 'Phase', 'Month2_Retention']].head(5).round(2))

# Month-2 Retention by Cohort
cohorts_at_risk_plot = (cohorts_at_risk.set_index('CohortMonth'))
plt.figure(figsize=(10, 5))

cohorts_at_risk_plot['Month2_Retention'].plot(kind='bar')
plt.title('Month-2 Retention by Customer Cohort')
plt.xlabel('Customer Acquisition Cohort')
plt.ylabel('Month-2 Retention (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


print("\nPre-Crisis vs Crisis Retention:")
print(retention_comparison.round(2))

print(f"\nRetention decline: " f"{retention_decline:.2f} percentage points")
print(f"Relative retention decline: "f"{relative_decline:.2f}%")
print("\nTop 5 Cohorts at Risk:")
print(cohorts_at_risk.head(5).round(2))


print("\n" + "="*60)
print("FINAL ANALYSIS SUMMARY")
print("="*60)

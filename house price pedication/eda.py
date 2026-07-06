import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('house_data.csv')

print("=" * 50)
print("DATASET OVERVIEW")
print("=" * 50)
print(f"Shape     : {df.shape}")
print(f"Columns   : {list(df.columns)}")
print("\nFirst 5 rows:")
print(df.head())
print("\nBasic Statistics:")
print(df.describe())
print("\nMissing Values:")
print(df.isnull().sum())

# ── Plots ──────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('House Price Prediction – EDA', fontsize=16, fontweight='bold')

# 1. Price distribution
axes[0, 0].hist(df['price_lakhs'], bins=40, color='steelblue', edgecolor='white')
axes[0, 0].set_title('Price Distribution (Lakhs)')
axes[0, 0].set_xlabel('Price (Lakhs)')

# 2. Area vs Price
axes[0, 1].scatter(df['area_sqft'], df['price_lakhs'], alpha=0.4, color='coral')
axes[0, 1].set_title('Area vs Price')
axes[0, 1].set_xlabel('Area (sqft)')
axes[0, 1].set_ylabel('Price (Lakhs)')

# 3. Bedrooms vs avg price
avg_price = df.groupby('bedrooms')['price_lakhs'].mean()
axes[0, 2].bar(avg_price.index, avg_price.values, color='teal')
axes[0, 2].set_title('Avg Price by Bedrooms')
axes[0, 2].set_xlabel('Bedrooms')

# 4. Distance vs Price
axes[1, 0].scatter(df['distance_km'], df['price_lakhs'], alpha=0.4, color='purple')
axes[1, 0].set_title('Distance from City vs Price')
axes[1, 0].set_xlabel('Distance (km)')

# 5. Location score vs Price
axes[1, 1].scatter(df['location_score'], df['price_lakhs'], alpha=0.4, color='orange')
axes[1, 1].set_title('Location Score vs Price')
axes[1, 1].set_xlabel('Location Score')

# 6. Correlation heatmap
corr = df.corr()
sns.heatmap(corr, ax=axes[1, 2], annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
axes[1, 2].set_title('Correlation Heatmap')

plt.tight_layout()
plt.savefig('eda_plots.png', dpi=150)
plt.show()
print("\nEDA plots saved → eda_plots.png")

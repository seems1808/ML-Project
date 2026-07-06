import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

cities = [
    'Mumbai', 'Pune', 'Nashik', 'Nagpur', 'Aurangabad',
    'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata'
]

data = {
    'city':           np.random.choice(cities, n),
    'area_sqft':      np.random.randint(500, 5000, n),
    'bedrooms':       np.random.randint(1, 6, n),
    'bathrooms':      np.random.randint(1, 4, n),
    'age_years':      np.random.randint(0, 50, n),
    'distance_km':    np.round(np.random.uniform(1, 30, n), 1),
    'floor':          np.random.randint(0, 20, n),
    'parking':        np.random.randint(0, 3, n),
    'location_score': np.random.randint(1, 10, n),
    'furnished':      np.random.randint(0, 2, n),
}

df = pd.DataFrame(data)

# City price multiplier (metro cities cost more)
city_multiplier = {
    'Mumbai': 2.5, 'Delhi': 2.2, 'Bangalore': 2.0,
    'Hyderabad': 1.8, 'Chennai': 1.7, 'Kolkata': 1.5,
    'Pune': 1.4, 'Nagpur': 1.1, 'Nashik': 1.0, 'Aurangabad': 0.9
}
df['city_factor'] = df['city'].map(city_multiplier)

df['price_lakhs'] = (
    df['area_sqft'] * 0.04
    + df['bedrooms'] * 3
    + df['bathrooms'] * 2
    - df['age_years'] * 0.5
    - df['distance_km'] * 1.2
    + df['floor'] * 0.8
    + df['parking'] * 2
    + df['location_score'] * 5
    + df['furnished'] * 4
    + np.random.normal(0, 5, n)
) * df['city_factor']

df['price_lakhs'] = df['price_lakhs'].round(2).clip(lower=10)
df.drop(columns=['city_factor'], inplace=True)

df.to_csv('house_data.csv', index=False)
print(f"Dataset created: {len(df)} rows")
print(f"Cities included: {cities}")
print(df.head())

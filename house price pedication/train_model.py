import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ── Load data ─────────────────────────────────────
df = pd.read_csv('house_data.csv')

FEATURES = [
    'area_sqft', 'bedrooms', 'bathrooms', 'age_years',
    'distance_km', 'floor', 'parking', 'location_score', 'furnished'
]
TARGET = 'price_lakhs'

X = df[FEATURES]
y = df[TARGET]

# ── Split ──────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Scale ──────────────────────────────────────────
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ── Models ─────────────────────────────────────────
models = {
    'Linear Regression':       LinearRegression(),
    'Random Forest':           RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting':       GradientBoostingRegressor(n_estimators=100, random_state=42),
}

print("=" * 60)
print(f"{'Model':<25} {'MAE':>8} {'RMSE':>8} {'R² Score':>10}")
print("=" * 60)

results = {}
for name, model in models.items():
    if name == 'Linear Regression':
        model.fit(X_train_sc, y_train)
        preds = model.predict(X_test_sc)
    else:
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

    mae  = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2   = r2_score(y_test, preds)

    results[name] = {'model': model, 'MAE': mae, 'RMSE': rmse, 'R2': r2}
    print(f"{name:<25} {mae:>8.2f} {rmse:>8.2f} {r2:>10.4f}")

print("=" * 60)

# ── Save best model (Random Forest) ───────────────
best_model  = results['Random Forest']['model']
with open('model.pkl',  'wb') as f: pickle.dump(best_model, f)
with open('scaler.pkl', 'wb') as f: pickle.dump(scaler, f)

print("\nBest model saved → model.pkl")
print("Scaler saved     → scaler.pkl")

# ── Feature importance ─────────────────────────────
importances = pd.Series(
    best_model.feature_importances_, index=FEATURES
).sort_values(ascending=False)

print("\nFeature Importances (Random Forest):")
for feat, imp in importances.items():
    bar = '█' * int(imp * 50)
    print(f"  {feat:<18} {imp:.4f}  {bar}")

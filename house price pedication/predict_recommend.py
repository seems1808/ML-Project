import pandas as pd
import pickle

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Load dataset
df = pd.read_csv("house_data.csv")

FEATURES = [
    "area_sqft",
    "bedrooms",
    "bathrooms",
    "age_years",
    "distance_km",
    "floor",
    "parking",
    "location_score",
    "furnished"
]

def recommend_houses(
    city,
    budget_lakhs,
    preferred_bedrooms=None,
    preferred_area=None,
    max_distance=None,
    preferred_floor=None,
    furnished=None,
    top_n=5
):

    filtered = df[df["city"].str.lower() == city.lower()].copy()

    if filtered.empty:
        return pd.DataFrame()

    filtered["predicted_price"] = model.predict(filtered[FEATURES])

    filtered = filtered[filtered["predicted_price"] <= budget_lakhs]

    if preferred_bedrooms is not None:
        filtered = filtered[filtered["bedrooms"] >= preferred_bedrooms]

    if preferred_area is not None:
        filtered = filtered[filtered["area_sqft"] >= preferred_area]

    if max_distance is not None:
        filtered = filtered[filtered["distance_km"] <= max_distance]

    if preferred_floor is not None:
        filtered = filtered[filtered["floor"] == preferred_floor]

    if furnished is not None:
        filtered = filtered[filtered["furnished"] == furnished]

    if filtered.empty:
        return pd.DataFrame()

    # ✅ SCORE (fixed indentation)
    filtered["score"] = (
        filtered["location_score"] * 3 +
        filtered["bedrooms"] * 2 +
        filtered["bathrooms"] * 1.5 +
        (filtered["area_sqft"] / 1000) * 2
    )

    # ✅ SORT
    filtered = filtered.sort_values(
        by=["score", "predicted_price"],
        ascending=[False, True]
    )

    # ✅ RESULT
    result = filtered[
        [
            "city",
            "area_sqft",
            "bedrooms",
            "bathrooms",
            "age_years",
            "distance_km",
            "floor",
            "parking",
            "location_score",
            "furnished",
            "predicted_price"
        ]
    ].head(top_n)

    result = result.reset_index(drop=True)

    result["furnished"] = result["furnished"].map({1: "Yes", 0: "No"})
    result["parking"] = result["parking"].map({1: "Yes", 0: "No"})
    result["predicted_price"] = result["predicted_price"].round(2)

    return result


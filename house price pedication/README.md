# 🏠 House Price Prediction & Recommendation System

A complete ML project using Linear Regression, Random Forest, and Gradient Boosting.

---

## 📁 Project Structure

```
house_price_prediction/
│
├── generate_dataset.py   ← Step 1: Creates house_data.csv
├── eda.py                ← Step 2: Exploratory Data Analysis + plots
├── train_model.py        ← Step 3: Train & compare 3 ML models
├── predict_recommend.py  ← Step 4: Predict price + get recommendations
├── requirements.txt      ← All dependencies
└── README.md
```

---

## ▶️ How to Run (Step by Step)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate dataset
```bash
python generate_dataset.py
```
Creates `house_data.csv` with 1000 sample house records.

### 3. Explore the data
```bash
python eda.py
```
Prints statistics and saves `eda_plots.png`.

### 4. Train the model
```bash
python train_model.py
```
Trains 3 models, prints comparison, saves `model.pkl` and `scaler.pkl`.

### 5. Predict & get recommendations
```bash
python predict_recommend.py
```
Predicts price for a sample house and shows top 5 recommendations.

---

## 🧠 Models Used

| Model               | Description                          |
|---------------------|--------------------------------------|
| Linear Regression   | Simple baseline model                |
| Random Forest       | Best performer — saved as model.pkl  |
| Gradient Boosting   | Ensemble of decision trees           |

---

## 🏷️ Features Used

| Feature        | Description                        |
|----------------|------------------------------------|
| area_sqft      | Total area in square feet          |
| bedrooms       | Number of bedrooms                 |
| bathrooms      | Number of bathrooms                |
| age_years      | Age of the property                |
| distance_km    | Distance from city center (km)     |
| floor          | Floor number                       |
| parking        | Number of parking spots            |
| location_score | Location rating (1–10)             |
| furnished      | 0 = Unfurnished, 1 = Furnished     |

---

## 🔧 Customize Recommendations

Edit `predict_recommend.py` and change these values:

```python
recs = recommend_houses(
    budget_lakhs=80,        # your budget
    preferred_area=1000,    # minimum area (sqft)
    preferred_bedrooms=2,   # minimum bedrooms
    max_distance=15,        # max distance from city (km)
    top_n=5                 # number of results
)
```

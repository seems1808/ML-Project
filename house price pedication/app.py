import streamlit as st
from predict_recommend import recommend_houses
import matplotlib.pyplot as plt

def calculate_emi(principal, annual_rate, years):
    monthly_rate = annual_rate / (12 * 100)
    months = years * 12

    if monthly_rate == 0:
        return principal / months

    emi = (
        principal * monthly_rate * (1 + monthly_rate) ** months
    ) / (
        (1 + monthly_rate) ** months - 1
    )

    return emi


st.title("🏠 House Recommendation System")

city = st.text_input("City")

budget = st.number_input("Budget (Lakhs)", 1.0, 500.0, 50.0)

bedrooms = st.number_input("Min Bedrooms", 1, 10, 2)

area = st.number_input("Min Area (sqft)", 500, 10000, 1000)

distance = st.number_input("Max Distance (km)", 0.0, 50.0, 10.0)

floor = st.number_input("Preferred Floor (optional)", 0, 50, 0)

furnished = st.selectbox("Furnished", ["Any", "Yes", "No"])

st.subheader("💰 EMI Calculator Settings")

down_payment_percent = st.slider("Down Payment (%)", 10, 90, 20)
interest_rate = st.number_input("Interest Rate (%)", 5.0, 20.0, 8.5)
loan_years = st.number_input("Loan Tenure (Years)", 5, 30, 20)


if st.button("Recommend"):

    furnished_val = None
    if furnished == "Yes":
        furnished_val = 1
    elif furnished == "No":
        furnished_val = 0

    result = recommend_houses(
        city=city,
        budget_lakhs=budget,
        preferred_bedrooms=bedrooms,
        preferred_area=area,
        max_distance=distance,
        preferred_floor=floor,
        furnished=furnished_val
    )

    if result.empty:
        st.warning("No houses found")

    else:
        st.success("Recommendations ready")

        # ---------------- EMI CALCULATION ----------------
        emi_list = []

        for price in result["predicted_price"]:
            price_rupees = price * 100000

            loan_amount = price_rupees * (1 - down_payment_percent / 100)

            emi = calculate_emi(
                loan_amount,
                interest_rate,
                loan_years
            )

            emi_list.append(round(emi, 2))

        result["Monthly EMI (₹)"] = emi_list

        # ---------------- TABLE ----------------
        st.dataframe(result)

        # ---------------- GRAPH ----------------
        st.subheader("📊 Price Comparison")

        fig, ax = plt.subplots()
        ax.bar(result["city"], result["predicted_price"])
        plt.xticks(rotation=45)

        st.pyplot(fig)
        
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SaaS Unit Economics", layout="centered")
st.title("📊 SaaS Unit Economics Calculator")

# Scenario selector
scenario = st.radio(
    "Choose a Scenario",
    ["Base", "Best Case", "Worst Case"],
    horizontal=True
)

# Default values per scenario
defaults = {
    "Base": {
        "ARPU": 200,
        "Gross Margin %": 80,
        "Lifetime": 24,
        "Spend": 50000,
        "Customers": 250
    },
    "Best Case": {
        "ARPU": 250,
        "Gross Margin %": 85,
        "Lifetime": 30,
        "Spend": 40000,
        "Customers": 300
    },
    "Worst Case": {
        "ARPU": 150,
        "Gross Margin %": 70,
        "Lifetime": 18,
        "Spend": 60000,
        "Customers": 200
    }
}

# Get scenario inputs
ARPU = st.number_input("ARPU (Monthly Revenue per Customer)", min_value=0.0, value=defaults[scenario]["ARPU"])
gross_margin_pct = st.slider("Gross Margin %", 0, 100, value=defaults[scenario]["Gross Margin %"]) / 100
customer_lifetime = st.number_input("Customer Lifetime (months)", 1, 120, value=defaults[scenario]["Lifetime"])
sales_spend = st.number_input("Sales & Marketing Spend ($)", 0.0, 1e6, value=defaults[scenario]["Spend"])
new_customers = st.number_input("New Customers Acquired", 1, 100000, value=defaults[scenario]["Customers"])

# Calculations
monthly_gm_per_cust = ARPU * gross_margin_pct
CAC = sales_spend / new_customers
LTV = ARPU * gross_margin_pct * customer_lifetime
LTV_CAC = LTV / CAC
payback = CAC / monthly_gm_per_cust

# Output table
results_df = pd.DataFrame({
    "Metric": [
        "Monthly GM per Customer",
        "Customer Acquisition Cost (CAC)",
        "Customer Lifetime Value (LTV)",
        "LTV:CAC Ratio",
        "Payback Period (Months)"
    ],
    "Value": [
        f"${monthly_gm_per_cust:,.2f}",
        f"${CAC:,.2f}",
        f"${LTV:,.2f}",
        f"{LTV_CAC:.2f}x",
        f"{payback:.2f} months"
    ]
})

st.subheader("📉 Unit Economics")
st.table(results_df)

# Chart
st.subheader("📊 Visual Comparison")

metrics_chart = pd.DataFrame({
    "Metric": ["LTV", "CAC", "Payback Period (mo)"],
    "Value": [LTV, CAC, payback]
})

fig, ax = plt.subplots()
ax.bar(metrics_chart["Metric"], metrics_chart["Value"])
ax.set_ylabel("Value ($ / Months)")
ax.set_title("Key Unit Economics")
st.pyplot(fig)

st.caption("Use the scenario selector and inputs to test your business model’s efficiency.")

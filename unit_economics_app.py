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

# Get scenario inputs (cast types to avoid StreamlitMixedNumericTypesError)
ARPU = st.number_input("ARPU (Monthly Revenue per Customer)", min_value=0.0, value=float(defaults[scenario]["ARPU"]))
gross_margin_pct = st.slider("Gross Margin %", 0, 100, value=int(defaults[scenario]["Gross Margin %"])) / 100
customer_lifetime = st.number_input("Customer Lifetime (months)", min_value=1, value=int(defaults[scenario]["Lifetime"]))
sales_spend = st.number_input("Sales & Marketing Spend ($)", min_value=0.0, value=float(defaults[scenario]["Spend"]))
new_customers = st.number_input("New Customers Acquired", min_value=1, value=int(defaults[scenario]["Customers"]))

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


# --- Multi-Year Cash Flow Modeling ---
st.subheader("📆 Multi-Year Cash Flow Forecast")

years = [1, 2, 3, 4, 5]
growth_rate = st.slider("Annual New Customer Growth Rate (%)", 0, 100, 20) / 100

# Starting base
customers_by_year = [new_customers]
for i in range(1, len(years)):
    customers_by_year.append(customers_by_year[-1] * (1 + growth_rate))

revenues = [ARPU * 12 * c for c in customers_by_year]
gross_profits = [rev * gross_margin_pct for rev in revenues]
cac_spend = [c * CAC for c in customers_by_year]
net_cash_flow = [gp - cac for gp, cac in zip(gross_profits, cac_spend)]

# Create DataFrame
forecast_df = pd.DataFrame({
    "Year": years,
    "New Customers": [int(c) for c in customers_by_year],
    "Revenue ($)": revenues,
    "Gross Profit ($)": gross_profits,
    "CAC Spend ($)": cac_spend,
    "Net Cash Flow ($)": net_cash_flow
})

st.dataframe(forecast_df.style.format({
    "Revenue ($)": "${:,.0f}",
    "Gross Profit ($)": "${:,.0f}",
    "CAC Spend ($)": "${:,.0f}",
    "Net Cash Flow ($)": "${:,.0f}"
}))

# Chart
st.subheader("📈 Cash Flow Trend Over Time")
fig2, ax2 = plt.subplots()
ax2.plot(years, net_cash_flow, marker='o', label="Net Cash Flow")
ax2.plot(years, revenues, linestyle='--', label="Revenue")
ax2.plot(years, cac_spend, linestyle='--', label="CAC Spend")
ax2.set_ylabel("Amount ($)")
ax2.set_xlabel("Year")
ax2.set_title("Cash Flow Forecast")
ax2.legend()
st.pyplot(fig2)


# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 0.9em; color: gray;'>"
    "Built by <a href='https://www.linkedin.com/in/timphamtx' target='_blank'>Tim Pham</a>"
    "</div>",
    unsafe_allow_html=True
)

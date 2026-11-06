
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px  

from utils.style import (
    apply_dashboard_style,
    render_kpi_card,
    apply_chart_style
)
from utils.data_loader import load_data


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Analysis",
    page_icon="👥",
    layout="wide"
)

apply_dashboard_style()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = load_data()


# --------------------------------------------------
# CUSTOMER ANALYSIS
# --------------------------------------------------

customer_analysis = (
    df.groupby("Customer Id")
    .agg(
        Customer_Segment=("Customer Segment", "first"),
        Net_Revenue=("Net Revenue", "sum"),
        Total_Profit=("Benefit per order", "sum"),
        Total_Records=("Customer Id", "count"),
        Average_Profit=("Benefit per order", "mean"),
        Loss_Records=(
            "Benefit per order",
            lambda x: (x < 0).sum()
        )
    )
    .reset_index()
)

customer_analysis["Profit_Margin"] = (
    customer_analysis["Total_Profit"]
    / customer_analysis["Net_Revenue"]
) * 100


# --------------------------------------------------
# CUSTOMER VALUE INDEX (CVI)
# --------------------------------------------------

customer_analysis["Profit_Score"] = (
    customer_analysis["Total_Profit"].rank(pct=True) * 100
)

customer_analysis["Revenue_Score"] = (
    customer_analysis["Net_Revenue"].rank(pct=True) * 100
)

customer_analysis["Frequency_Score"] = (
    customer_analysis["Total_Records"].rank(pct=True) * 100
)

customer_analysis["CVI"] = (
    0.50 * customer_analysis["Profit_Score"]
    + 0.30 * customer_analysis["Revenue_Score"]
    + 0.20 * customer_analysis["Frequency_Score"]
)

customer_analysis["Customer_Value_Category"] = np.where(
    customer_analysis["Total_Profit"] < 0,
    "Loss-making",
    np.where(
        customer_analysis["CVI"] >= 80,
        "High Value",
        np.where(
            customer_analysis["CVI"] >= 40,
            "Medium Value",
            "Low Value"
        )
    )
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("👥 Customer Value Analysis")

st.markdown(
    "### Customer Profitability, Segmentation and Value Index"
)

st.caption(
    "Understand customer contribution, identify high-value "
    "customers and evaluate loss-making customer groups."
)

st.divider()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Customer Filters")

segments = sorted(
    customer_analysis["Customer_Segment"].dropna().unique()
)

selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    segments,
    default=segments
)

value_categories = [
    "High Value",
    "Medium Value",
    "Low Value",
    "Loss-making"
]

selected_values = st.sidebar.multiselect(
    "Customer Value Category",
    value_categories,
    default=value_categories
)

filtered_customers = customer_analysis[
    customer_analysis["Customer_Segment"].isin(selected_segments)
    & customer_analysis["Customer_Value_Category"].isin(selected_values)
].copy()

if filtered_customers.empty:
    st.warning("No customers found for the selected filters.")
    st.stop()


# --------------------------------------------------
# MODERN CUSTOMER KPI CARDS
# --------------------------------------------------

st.subheader("Customer Performance Overview")

total_customers = len(filtered_customers)
total_customer_revenue = filtered_customers["Net_Revenue"].sum()
total_customer_profit = filtered_customers["Total_Profit"].sum()
avg_customer_profit = filtered_customers["Total_Profit"].mean()

high_value_count = (
    filtered_customers["Customer_Value_Category"] == "High Value"
).sum()

loss_customer_count = (
    filtered_customers["Customer_Value_Category"] == "Loss-making"
).sum()


c1, c2, c3 = st.columns(3)

with c1:
    render_kpi_card("Total Customers", f"{total_customers:,}")

with c2:
    render_kpi_card("Net Revenue", f"{total_customer_revenue:,.2f}")

with c3:
    render_kpi_card("Total Profit", f"{total_customer_profit:,.2f}")


c4, c5, c6 = st.columns(3)

with c4:
    render_kpi_card(
        "Average Profit / Customer",
        f"{avg_customer_profit:,.2f}"
    )

with c5:
    render_kpi_card("High-Value Customers", f"{high_value_count:,}")

with c6:
    render_kpi_card("Loss-making Customers", f"{loss_customer_count:,}")


st.divider()


# --------------------------------------------------
# CUSTOMER VALUE DISTRIBUTION
# --------------------------------------------------

st.subheader("Customer Value Distribution")

value_summary = (
    filtered_customers["Customer_Value_Category"]
    .value_counts()
    .reindex(value_categories, fill_value=0)
    .reset_index()
)

value_summary.columns = [
    "Customer Value Category",
    "Customers"
]

fig_value = px.pie(
    value_summary,
    names="Customer Value Category",
    values="Customers",
    hole=0.55,
    title="Customer Distribution by Value Category"
)

fig_value = apply_chart_style(fig_value)

st.plotly_chart(
    fig_value,
    use_container_width=True
)


# --------------------------------------------------
# SEGMENT-WISE PROFITABILITY
# --------------------------------------------------

st.subheader("Customer Segment Performance")

segment_analysis = (
    filtered_customers.groupby("Customer_Segment")
    .agg(
        Customers=("Customer Id", "count"),
        Net_Revenue=("Net_Revenue", "sum"),
        Total_Profit=("Total_Profit", "sum")
    )
    .reset_index()
)

segment_analysis["Profit_Margin"] = (
    segment_analysis["Total_Profit"]
    / segment_analysis["Net_Revenue"] * 100
)


col1, col2 = st.columns(2)

with col1:

    fig_segment = px.bar(
        segment_analysis,
        x="Customer_Segment",
        y="Total_Profit",
        title="Total Profit by Customer Segment",
        text_auto=".2s"
    )

    fig_segment = apply_chart_style(fig_segment)

    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )


with col2:

    fig_margin = px.bar(
        segment_analysis,
        x="Customer_Segment",
        y="Profit_Margin",
        title="Profit Margin by Customer Segment",
        text_auto=".2f"
    )

    fig_margin = apply_chart_style(fig_margin)

    st.plotly_chart(
        fig_margin,
        use_container_width=True
    )


# --------------------------------------------------
# TOP PROFITABLE CUSTOMERS
# --------------------------------------------------

st.subheader("Top 10 Profitable Customers")

top_customers = (
    filtered_customers.sort_values(
        "Total_Profit",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_customers[
        [
            "Customer Id",
            "Customer_Segment",
            "Net_Revenue",
            "Total_Profit",
            "Profit_Margin",
            "CVI",
            "Customer_Value_Category"
        ]
    ].round(2),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# LOSS-MAKING CUSTOMERS
# --------------------------------------------------

st.subheader("Top 10 Loss-making Customers")

loss_customers = (
    filtered_customers[
        filtered_customers["Total_Profit"] < 0
    ]
    .sort_values("Total_Profit")
    .head(10)
)

st.dataframe(
    loss_customers[
        [
            "Customer Id",
            "Customer_Segment",
            "Net_Revenue",
            "Total_Profit",
            "Profit_Margin",
            "CVI"
        ]
    ].round(2),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# CUSTOMER VALUE SUMMARY
# --------------------------------------------------

st.subheader("Customer Value Summary")

value_table = (
    filtered_customers.groupby("Customer_Value_Category")
    .agg(
        Customers=("Customer Id", "count"),
        Net_Revenue=("Net_Revenue", "sum"),
        Total_Profit=("Total_Profit", "sum"),
        Average_CVI=("CVI", "mean")
    )
    .reset_index()
)

st.dataframe(
    value_table.round(2),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Customer Value Analysis | Supply Chain Profitability Analytics"
)

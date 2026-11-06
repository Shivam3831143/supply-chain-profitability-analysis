
import streamlit as st
import pandas as pd
from importlib import import_module

from utils.style import (
    apply_dashboard_style,
    render_kpi_card,
    apply_chart_style
)

from utils.data_loader import load_data

px = import_module("plotly.express")


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Supply Chain Profitability Analytics",
    page_icon="📊",
    layout="wide"
)

apply_dashboard_style()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = load_data()


# --------------------------------------------------
# DASHBOARD HEADER
# --------------------------------------------------

st.title("📊 Supply Chain Profitability Analytics")

st.markdown(
    "### Revenue, Profitability and Business Performance Dashboard"
)

st.caption(
    "An interactive analysis of customer, product, market "
    "and financial performance."
)

st.divider()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

selected_markets = st.sidebar.multiselect(
    "Select Market",
    options=sorted(df["Market"].dropna().unique()),
    default=sorted(df["Market"].dropna().unique())
)

selected_segments = st.sidebar.multiselect(
    "Select Customer Segment",
    options=sorted(df["Customer Segment"].dropna().unique()),
    default=sorted(df["Customer Segment"].dropna().unique())
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category Name"].dropna().unique()),
    default=sorted(df["Category Name"].dropna().unique())
)


# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

filtered_df = df[
    (df["Market"].isin(selected_markets)) &
    (df["Customer Segment"].isin(selected_segments)) &
    (df["Category Name"].isin(selected_categories))
].copy()


if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_gross_sales = filtered_df["Sales"].sum()

total_net_revenue = filtered_df["Net Revenue"].sum()

total_profit = filtered_df["Benefit per order"].sum()

profit_margin = (
    total_profit / total_net_revenue * 100
    if total_net_revenue != 0 else 0
)

total_records = len(filtered_df)

unique_customers = filtered_df["Customer Id"].nunique()


# --------------------------------------------------
# MODERN KPI CARDS
# --------------------------------------------------

st.subheader("Business Performance Overview")

col1, col2, col3 = st.columns(3)

with col1:
    render_kpi_card(
        "Gross Sales",
        f"{total_gross_sales:,.2f}"
    )

with col2:
    render_kpi_card(
        "Net Revenue",
        f"{total_net_revenue:,.2f}"
    )

with col3:
    render_kpi_card(
        "Total Profit",
        f"{total_profit:,.2f}"
    )


col4, col5, col6 = st.columns(3)

with col4:
    render_kpi_card(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )

with col5:
    render_kpi_card(
        "Total Transactions",
        f"{total_records:,}"
    )

with col6:
    render_kpi_card(
        "Unique Customers",
        f"{unique_customers:,}"
    )

st.divider()


# --------------------------------------------------
# PROFITABILITY DISTRIBUTION
# --------------------------------------------------

st.subheader("Profitability Distribution")

profit_counts = (
    filtered_df["Profit Status"]
    .value_counts()
    .reset_index()
)

profit_counts.columns = ["Profit Status", "Records"]

fig_profit = px.pie(
    profit_counts,
    names="Profit Status",
    values="Records",
    hole=0.55,
    title="Distribution of Profitable and Loss-making Records"
)

fig_profit = apply_chart_style(fig_profit)

st.plotly_chart(
    fig_profit,
    use_container_width=True
)


# --------------------------------------------------
# MARKET-WISE PERFORMANCE
# --------------------------------------------------

st.subheader("Market-wise Performance")

market_analysis = (
    filtered_df.groupby("Market")
    .agg(
        Net_Revenue=("Net Revenue", "sum"),
        Total_Profit=("Benefit per order", "sum")
    )
    .reset_index()
)

col1, col2 = st.columns(2)


# Net Revenue Chart

with col1:

    fig_revenue = px.bar(
        market_analysis.sort_values(
            "Net_Revenue", ascending=False
        ),
        x="Market",
        y="Net_Revenue",
        title="Net Revenue by Market",
        text_auto=".2s",
        labels={
            "Net_Revenue": "Net Revenue",
            "Market": "Market"
        }
    )

    fig_revenue.update_layout(
        xaxis_title="Market",
        yaxis_title="Net Revenue",
        showlegend=False
    )

    fig_revenue = apply_chart_style(fig_revenue)

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )


# Total Profit Chart

with col2:

    fig_profit_market = px.bar(
        market_analysis.sort_values(
            "Total_Profit", ascending=False
        ),
        x="Market",
        y="Total_Profit",
        title="Total Profit by Market",
        text_auto=".2s",
        labels={
            "Total_Profit": "Total Profit",
            "Market": "Market"
        }
    )

    fig_profit_market.update_layout(
        xaxis_title="Market",
        yaxis_title="Total Profit",
        showlegend=False
    )

    fig_profit_market = apply_chart_style(fig_profit_market)

    st.plotly_chart(
        fig_profit_market,
        use_container_width=True
    )


# --------------------------------------------------
# CATEGORY-WISE PERFORMANCE
# --------------------------------------------------

st.subheader("Category-wise Profitability")

category_analysis = (
    filtered_df.groupby("Category Name")
    .agg(
        Net_Revenue=("Net Revenue", "sum"),
        Total_Profit=("Benefit per order", "sum")
    )
    .reset_index()
    .sort_values("Total_Profit", ascending=False)
)

fig_category = px.bar(
    category_analysis.head(10),
    x="Total_Profit",
    y="Category Name",
    orientation="h",
    title="Top 10 Categories by Total Profit",
    labels={
        "Total_Profit": "Total Profit",
        "Category Name": "Product Category"
    }
)

fig_category.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

fig_category = apply_chart_style(fig_category)

st.plotly_chart(
    fig_category,
    use_container_width=True
)


# --------------------------------------------------
# DETAILED MARKET TABLE
# --------------------------------------------------

st.subheader("Market Performance Details")

market_analysis["Profit_Margin"] = (
    market_analysis["Total_Profit"] /
    market_analysis["Net_Revenue"] * 100
)

st.dataframe(
    market_analysis.round(2),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Supply Chain Profitability Analytics | "
    "Developed using Python, Pandas, Streamlit and Plotly"
)

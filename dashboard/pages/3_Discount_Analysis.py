
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
    page_title="Discount Analysis",
    page_icon="💰",
    layout="wide"
)

apply_dashboard_style()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = load_data()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("💰 Discount Impact Analyzer")

st.subheader(
    "Discount Strategy, Profitability and Loss Analysis"
)

st.caption(
    "Understand how different discount levels are associated "
    "with revenue, profit margins and transaction losses."
)

st.divider()


# --------------------------------------------------
# CREATE DISCOUNT BANDS
# --------------------------------------------------

df["Discount_Band"] = pd.cut(
    df["Order Item Discount Rate"],
    bins=[-0.001, 0, 0.05, 0.10, 0.15, 0.20, 0.251],
    labels=[
        "0% Discount",
        "Above 0-5%",
        "Above 5-10%",
        "Above 10-15%",
        "Above 15-20%",
        "Above 20-25%"
    ],
    include_lowest=True
)

discount_order = [
    "0% Discount",
    "Above 0-5%",
    "Above 5-10%",
    "Above 10-15%",
    "Above 15-20%",
    "Above 20-25%"
]


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Discount Filters")

markets = sorted(df["Market"].dropna().unique())
segments = sorted(df["Customer Segment"].dropna().unique())
categories = sorted(df["Category Name"].dropna().unique())

selected_markets = st.sidebar.multiselect(
    "Select Market",
    markets,
    default=markets
)

selected_segments = st.sidebar.multiselect(
    "Select Customer Segment",
    segments,
    default=segments
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df[
    df["Market"].isin(selected_markets)
    & df["Customer Segment"].isin(selected_segments)
    & df["Category Name"].isin(selected_categories)
].copy()

if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()


# --------------------------------------------------
# DISCOUNT PERFORMANCE AGGREGATION
# --------------------------------------------------

discount_summary = (
    filtered_df.groupby("Discount_Band", observed=True)
    .agg(
        Net_Revenue=("Net Revenue", "sum"),
        Total_Profit=("Benefit per order", "sum"),
        Total_Records=("Discount_Band", "count"),
        Average_Discount=("Order Item Discount", "mean"),
        Loss_Records=(
            "Benefit per order",
            lambda x: (x < 0).sum()
        )
    )
    .reindex(discount_order)
    .reset_index()
)

discount_summary["Profit_Margin"] = (
    discount_summary["Total_Profit"] /
    discount_summary["Net_Revenue"].replace(0, np.nan)
) * 100

discount_summary["Loss_Rate"] = (
    discount_summary["Loss_Records"] /
    discount_summary["Total_Records"].replace(0, np.nan)
) * 100


# --------------------------------------------------
# KPI OVERVIEW
# --------------------------------------------------

st.header("Discount Performance Overview")

total_discount = filtered_df["Order Item Discount"].sum()

average_discount = filtered_df["Order Item Discount"].mean()

total_profit = filtered_df["Benefit per order"].sum()

total_net_revenue = filtered_df["Net Revenue"].sum()

overall_margin = (
    total_profit / total_net_revenue * 100
    if total_net_revenue != 0 else 0
)

loss_records = (
    filtered_df["Benefit per order"] < 0
).sum()


# --------------------------------------------------
# MODERN DISCOUNT KPI CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    render_kpi_card(
        "Total Discount Amount",
        f"{total_discount:,.2f}"
    )

with col2:
    render_kpi_card(
        "Average Discount Amount",
        f"{average_discount:,.2f}"
    )

with col3:
    render_kpi_card(
        "Overall Profit Margin",
        f"{overall_margin:.2f}%"
    )


col4, col5, col6 = st.columns(3)

with col4:
    render_kpi_card(
        "Total Net Revenue",
        f"{total_net_revenue:,.2f}"
    )

with col5:
    render_kpi_card(
        "Total Profit",
        f"{total_profit:,.2f}"
    )

with col6:
    render_kpi_card(
        "Loss-making Transactions",
        f"{loss_records:,}"
    )


st.divider()


# --------------------------------------------------
# PROFIT MARGIN BY DISCOUNT BAND
# --------------------------------------------------

st.header("Profit Margin by Discount Band")

fig_margin = px.bar(
    discount_summary,
    x="Discount_Band",
    y="Profit_Margin",
    text="Profit_Margin",
    title="Profit Margin Across Discount Levels",
    hover_data=[
        "Net_Revenue",
        "Total_Profit",
        "Total_Records"
    ]
)

fig_margin.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_margin.update_layout(
    xaxis_title="Discount Band",
    yaxis_title="Profit Margin (%)",
    yaxis_ticksuffix="%"
)

fig_margin = apply_chart_style(fig_margin)

st.plotly_chart(
    fig_margin,
    use_container_width=True
)


# --------------------------------------------------
# LOSS RATE BY DISCOUNT BAND
# --------------------------------------------------

st.header("Loss Rate Analysis")

fig_loss = px.line(
    discount_summary,
    x="Discount_Band",
    y="Loss_Rate",
    markers=True,
    text="Loss_Rate",
    title="Loss-making Transaction Rate by Discount Band"
)

fig_loss.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="top center"
)

fig_loss.update_layout(
    xaxis_title="Discount Band",
    yaxis_title="Loss Rate (%)",
    yaxis_ticksuffix="%"
)

fig_loss = apply_chart_style(fig_loss)

st.plotly_chart(
    fig_loss,
    use_container_width=True
)


# --------------------------------------------------
# CUSTOMER SEGMENT DISCOUNT ANALYSIS
# --------------------------------------------------

st.divider()

st.header("Customer Segment vs Discount Analysis")

segment_discount = (
    filtered_df.groupby(
        ["Customer Segment", "Discount_Band"],
        observed=True
    )
    .agg(
        Net_Revenue=("Net Revenue", "sum"),
        Total_Profit=("Benefit per order", "sum"),
        Total_Records=("Discount_Band", "count")
    )
    .reset_index()
)

segment_discount["Profit_Margin"] = (
    segment_discount["Total_Profit"] /
    segment_discount["Net_Revenue"].replace(0, np.nan)
) * 100

segment_pivot = segment_discount.pivot(
    index="Customer Segment",
    columns="Discount_Band",
    values="Profit_Margin"
).reindex(columns=discount_order)

fig_segment = px.imshow(
    segment_pivot,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="RdYlGn",
    labels={
        "x": "Discount Band",
        "y": "Customer Segment",
        "color": "Profit Margin (%)"
    },
    title="Customer Segment Profit Margin by Discount Band"
)

fig_segment = apply_chart_style(fig_segment)

st.plotly_chart(
    fig_segment,
    use_container_width=True
)


# --------------------------------------------------
# CATEGORY-WISE DISCOUNT IMPACT
# --------------------------------------------------

st.header("Category-wise Discount Impact")

category_discount = (
    filtered_df.groupby(
        ["Category Name", "Discount_Band"],
        observed=True
    )
    .agg(
        Net_Revenue=("Net Revenue", "sum"),
        Total_Profit=("Benefit per order", "sum"),
        Total_Records=("Discount_Band", "count")
    )
    .reset_index()
)

category_discount["Profit_Margin"] = (
    category_discount["Total_Profit"] /
    category_discount["Net_Revenue"].replace(0, np.nan)
) * 100

category_pivot = category_discount.pivot(
    index="Category Name",
    columns="Discount_Band",
    values="Profit_Margin"
).reindex(columns=discount_order)

fig_category = px.imshow(
    category_pivot,
    aspect="auto",
    color_continuous_scale="RdYlGn",
    labels={
        "x": "Discount Band",
        "y": "Category",
        "color": "Profit Margin (%)"
    },
    title="Category-wise Profit Margin Across Discount Bands"
)

fig_category = apply_chart_style(fig_category)

st.plotly_chart(
    fig_category,
    use_container_width=True
)


# --------------------------------------------------
# PRODUCT-WISE DISCOUNT IMPACT
# --------------------------------------------------

st.header("Product-wise Discount Impact")

product_discount = (
    filtered_df.groupby(
        ["Product Name", "Discount_Band"],
        observed=True
    )
    .agg(
        Net_Revenue=("Net Revenue", "sum"),
        Total_Profit=("Benefit per order", "sum"),
        Total_Records=("Discount_Band", "count")
    )
    .reset_index()
)

product_discount["Profit_Margin"] = (
    product_discount["Total_Profit"] /
    product_discount["Net_Revenue"].replace(0, np.nan)
) * 100

product_pivot = product_discount.pivot(
    index="Product Name",
    columns="Discount_Band",
    values="Profit_Margin"
).reindex(columns=discount_order)

st.write(
    "Select a product to compare its profitability across "
    "different discount levels."
)

available_products = sorted(
    product_discount["Product Name"].dropna().unique()
)

selected_product = st.selectbox(
    "Select Product",
    available_products
)

selected_product_data = product_discount[
    product_discount["Product Name"] == selected_product
].copy()

selected_product_data["Discount_Band"] = pd.Categorical(
    selected_product_data["Discount_Band"],
    categories=discount_order,
    ordered=True
)

selected_product_data = selected_product_data.sort_values(
    "Discount_Band"
)

fig_product = px.bar(
    selected_product_data,
    x="Discount_Band",
    y="Profit_Margin",
    text="Profit_Margin",
    title=f"Discount Impact: {selected_product}"
)

fig_product.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_product.update_layout(
    xaxis_title="Discount Band",
    yaxis_title="Profit Margin (%)"
)

fig_product = apply_chart_style(fig_product)

st.plotly_chart(
    fig_product,
    use_container_width=True
)


# --------------------------------------------------
# DISCOUNT SUMMARY TABLE
# --------------------------------------------------

st.divider()

st.header("Discount Performance Details")

st.dataframe(
    discount_summary.round(2),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Supply Chain Profitability Analytics | "
    "Discount Impact Analyzer | Python, Pandas, Streamlit and Plotly"
)

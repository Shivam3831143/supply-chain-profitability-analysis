
import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path

from utils.style import (
    apply_dashboard_style,
    render_kpi_card,
    apply_chart_style
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Product Analysis",
    page_icon="📦",
    layout="wide"
)

apply_dashboard_style()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📦 Product Analysis")
st.subheader("Product and Category Profitability Dashboard")

st.caption(
    "Analyze product performance, category contribution, "
    "revenue generation and profitability."
)

st.divider()


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

@st.cache_data
def load_data():
    project_root = Path(__file__).resolve().parents[2]
    file_path = project_root / "dataset" / "APL_Logistics_dataset.csv"

    data = pd.read_csv(file_path)

    # Net revenue is the amount after discount
    data["Net Revenue"] = data["Order Item Total"]

    return data


try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset not found. Please check the dataset folder.")
    st.stop()


# --------------------------------------------------
# DATA PREPARATION
# --------------------------------------------------

required_columns = [
    "Product Name",
    "Category Name",
    "Market",
    "Customer Segment",
    "Net Revenue",
    "Benefit per order",
    "Order Item Discount",
    "Order Item Discount Rate"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.stop()


# --------------------------------------------------
# PRODUCT FILTERS
# --------------------------------------------------

st.sidebar.header("Product Filters")

markets = sorted(df["Market"].dropna().unique())
segments = sorted(df["Customer Segment"].dropna().unique())
categories = sorted(df["Category Name"].dropna().unique())
products = sorted(df["Product Name"].dropna().unique())

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

selected_products = st.sidebar.multiselect(
    "Select Products",
    products,
    default=products
)


# Apply filters
filtered_df = df.copy()

if selected_markets:
    filtered_df = filtered_df[
        filtered_df["Market"].isin(selected_markets)
    ]

if selected_segments:
    filtered_df = filtered_df[
        filtered_df["Customer Segment"].isin(selected_segments)
    ]

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["Category Name"].isin(selected_categories)
    ]

if selected_products:
    filtered_df = filtered_df[
        filtered_df["Product Name"].isin(selected_products)
    ]

if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()


# --------------------------------------------------
# PRODUCT-LEVEL AGGREGATION
# --------------------------------------------------

product_summary = filtered_df.groupby(
    ["Product Name", "Category Name"],
    as_index=False
).agg(
    Net_Revenue=("Net Revenue", "sum"),
    Total_Profit=("Benefit per order", "sum"),
    Total_Records=("Product Name", "count"),
    Average_Profit=("Benefit per order", "mean"),
    Average_Discount=("Order Item Discount", "mean"),
    Loss_Records=(
        "Benefit per order",
        lambda x: (x < 0).sum()
    )
)

product_summary["Profit_Margin"] = (
    product_summary["Total_Profit"] /
    product_summary["Net_Revenue"].replace(0, pd.NA)
) * 100

product_summary["Loss_Rate"] = (
    product_summary["Loss_Records"] /
    product_summary["Total_Records"]
) * 100


# --------------------------------------------------
# CATEGORY-LEVEL AGGREGATION
# --------------------------------------------------

category_summary = filtered_df.groupby(
    "Category Name",
    as_index=False
).agg(
    Net_Revenue=("Net Revenue", "sum"),
    Total_Profit=("Benefit per order", "sum"),
    Total_Records=("Category Name", "count")
)

category_summary["Profit_Margin"] = (
    category_summary["Total_Profit"] /
    category_summary["Net_Revenue"].replace(0, pd.NA)
) * 100

category_summary = category_summary.sort_values(
    "Total_Profit",
    ascending=False
)


# --------------------------------------------------
# PRODUCT PERFORMANCE OVERVIEW
# --------------------------------------------------

st.header("Product Performance Overview")

total_products = filtered_df["Product Name"].nunique()
total_revenue = filtered_df["Net Revenue"].sum()
total_profit = filtered_df["Benefit per order"].sum()

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0 else 0
)

loss_products = (
    product_summary["Total_Profit"] < 0
).sum()


# --------------------------------------------------
# MODERN PRODUCT KPI CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    render_kpi_card(
        "Unique Products",
        f"{total_products:,}"
    )

with col2:
    render_kpi_card(
        "Net Revenue",
        f"{total_revenue:,.2f}"
    )

with col3:
    render_kpi_card(
        "Total Profit",
        f"{total_profit:,.2f}"
    )


col4, col5, col6 = st.columns(3)

with col4:
    render_kpi_card(
        "Overall Profit Margin",
        f"{profit_margin:.2f}%"
    )

with col5:
    render_kpi_card(
        "Loss-making Products",
        f"{loss_products:,}"
    )

with col6:
    render_kpi_card(
        "Total Transactions",
        f"{len(filtered_df):,}"
    )


st.divider()


# --------------------------------------------------
# TOP 10 PRODUCTS BY PROFIT
# --------------------------------------------------

st.header("Top Performing Products")

top_products = product_summary.nlargest(
    10,
    "Total_Profit"
)

fig_top = px.bar(
    top_products,
    x="Total_Profit",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Total Profit",
    text_auto=".2s",
    labels={
        "Total_Profit": "Total Profit",
        "Product Name": "Product"
    }
)

fig_top.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

fig_top = apply_chart_style(fig_top)

st.plotly_chart(
    fig_top,
    use_container_width=True
)


# --------------------------------------------------
# BOTTOM 10 PRODUCTS
# --------------------------------------------------

st.header("Products Requiring Attention")

bottom_products = product_summary.nsmallest(
    10,
    "Total_Profit"
)

fig_bottom = px.bar(
    bottom_products,
    x="Total_Profit",
    y="Product Name",
    orientation="h",
    title="Bottom 10 Products by Total Profit",
    text_auto=".2s",
    labels={
        "Total_Profit": "Total Profit",
        "Product Name": "Product"
    }
)

fig_bottom = apply_chart_style(fig_bottom)

st.plotly_chart(
    fig_bottom,
    use_container_width=True
)


# --------------------------------------------------
# CATEGORY-WISE PROFITABILITY
# --------------------------------------------------

st.divider()

st.header("Category-wise Profitability")

top_categories = category_summary.head(10)

fig_category = px.bar(
    top_categories,
    x="Category Name",
    y="Total_Profit",
    title="Top 10 Categories by Total Profit",
    text_auto=".2s",
    labels={
        "Category Name": "Category",
        "Total_Profit": "Total Profit"
    }
)

fig_category = apply_chart_style(fig_category)

st.plotly_chart(
    fig_category,
    use_container_width=True
)


# --------------------------------------------------
# PRODUCT REVENUE VS PROFIT
# --------------------------------------------------

st.header("Product Revenue vs Profit Analysis")

fig_scatter = px.scatter(
    product_summary,
    x="Net_Revenue",
    y="Total_Profit",
    color="Category Name",
    size="Total_Records",
    hover_name="Product Name",
    hover_data=[
        "Profit_Margin",
        "Total_Records"
    ],
    title="Product Revenue vs Profit",
    labels={
        "Net_Revenue": "Net Revenue",
        "Total_Profit": "Total Profit",
        "Category Name": "Category",
        "Total_Records": "Transactions"
    }
)

fig_scatter = apply_chart_style(fig_scatter)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# --------------------------------------------------
# PRODUCT PROFIT MARGIN
# --------------------------------------------------

st.header("Product Profit Margin Analysis")

margin_products = product_summary.sort_values(
    "Profit_Margin",
    ascending=False
).head(15)

fig_margin = px.bar(
    margin_products,
    x="Profit_Margin",
    y="Product Name",
    orientation="h",
    title="Top 15 Products by Profit Margin",
    text_auto=".2f",
    labels={
        "Profit_Margin": "Profit Margin (%)",
        "Product Name": "Product"
    }
)

fig_margin.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

fig_margin = apply_chart_style(fig_margin)

st.plotly_chart(
    fig_margin,
    use_container_width=True
)


# --------------------------------------------------
# PRODUCT PERFORMANCE TABLE
# --------------------------------------------------

st.divider()

st.header("Product Performance Details")

display_columns = [
    "Product Name",
    "Category Name",
    "Net_Revenue",
    "Total_Profit",
    "Profit_Margin",
    "Average_Profit",
    "Average_Discount",
    "Total_Records",
    "Loss_Records",
    "Loss_Rate"
]

st.dataframe(
    product_summary[
        display_columns
    ].sort_values(
        "Total_Profit",
        ascending=False
    ).round(2),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# CATEGORY PERFORMANCE TABLE
# --------------------------------------------------

st.header("Category Performance Details")

st.dataframe(
    category_summary.round(2),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Supply Chain Profitability Analytics | "
    "Product Analysis | Developed using Python, Pandas, "
    "Streamlit and Plotly"
)

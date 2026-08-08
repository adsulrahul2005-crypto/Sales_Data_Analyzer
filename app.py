import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Sales Data Analyzer",
    page_icon="📊",
    layout="wide"
)

# Load Data ---------------------------------------------------------------------------------------------
df = pd.read_csv("sales_data.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Create Sales column
df["Sales"] = df["Quantity"] * df["Price"]

# Title
st.title("📊 Sales Data Analyzer")
st.write("A simple Data Analyst dashboard using Python, Pandas and Streamlit")

st.divider()

# Sidebar Filters
st.sidebar.header("🔎 Filters")

categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

cities = ["All"] + sorted(df["City"].unique().tolist())
selected_city = st.sidebar.selectbox(
    "Select City",
    cities
)

# Filter Data-------------------------------------------------------------------------------------
filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

if selected_city != "All":
    filtered_df = filtered_df[
        filtered_df["City"] == selected_city
    ]

# KPIs --------------------------------------------------------------------------------------------
total_sales = filtered_df["Sales"].sum()
total_orders = len(filtered_df)

if total_orders > 0:
    average_order_value = total_sales / total_orders
else:
    average_order_value = 0

if not filtered_df.empty:
    best_product = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .idxmax()
    )
else:
    best_product = "No data"

# Display KPIs -----------------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "📦 Total Orders",
    total_orders
)

col3.metric(
    "📊 Average Order Value",
    f"₹{average_order_value:,.0f}"
)

col4.metric(
    "🏆 Best Product",
    best_product
)

st.divider()

# Sales by Category and City ----------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Sales by Category")

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)

with col2:
    st.subheader("🏙️ Sales by City")

    city_sales = (
        filtered_df
        .groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(city_sales)

# Monthly Sales --------------------------------------------------------------------------------------------
st.subheader("📅 Monthly Sales")

monthly_sales = (
    filtered_df
    .set_index("Date")
    .resample("ME")["Sales"]
    .sum()
)

st.line_chart(monthly_sales)

st.divider()

# Top Products -------------------------------------------------------------------------------
st.subheader("🏆 Top 5 Products")

product_sales = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(product_sales)

# Data Table --------------------------------------------------------------------------------------
st.subheader("📋 Sales Data")

columns = [
    "Order_ID",
    "Date",
    "Product",
    "Category",
    "City",
    "Quantity",
    "Price",
    "Sales"
]

st.dataframe(
    filtered_df[columns]
    .sort_values("Date", ascending=False),
    use_container_width=True,
    hide_index=True
)

# Business Insight ------------------------------------------------------------------------------------------
if not filtered_df.empty:

    top_city = (
        filtered_df
        .groupby("City")["Sales"]
        .sum()
        .idxmax()
    )

    top_category = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    st.info(
        f"💡 Insight: {top_city} has the highest sales, "
        f"and {top_category} is the highest-performing category."
    )

else:
    st.warning("No data found for the selected filters.")
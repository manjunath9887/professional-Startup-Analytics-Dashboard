import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("🚀 Startup Analytics")

industry = st.sidebar.multiselect(
    "Select Industry",
    df["Industry"].unique(),
    default=df["Industry"].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

exit_status = st.sidebar.multiselect(
    "Select Exit Status",
    df["Exit Status"].unique(),
    default=df["Exit Status"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region)) &
    (df["Exit Status"].isin(exit_status))
]

# ---------------------------
# Title
# ---------------------------
st.title("🚀 Startup Ecosystem Analytics Dashboard")

st.markdown("""
Comprehensive startup ecosystem analysis with funding,
valuation, profitability and market insights.
""")

# ---------------------------
# KPI Section
# ---------------------------
total_startups = len(filtered_df)

total_funding = filtered_df["Funding Amount (M USD)"].sum()

avg_valuation = filtered_df["Valuation (M USD)"].mean()

profitability_rate = (
    filtered_df["Profitable"].mean() * 100
)

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Total Startups",
    f"{total_startups:,}"
)

col2.metric(
    "Total Funding",
    f"${total_funding:,.2f} M"
)

col3.metric(
    "Average Valuation",
    f"${avg_valuation:,.2f} M"
)

col4.metric(
    "Profitability Rate",
    f"{profitability_rate:.2f}%"
)

st.divider()

# ---------------------------
# Industry Analysis
# ---------------------------
col1,col2 = st.columns(2)

with col1:

    industry_funding = (
        filtered_df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        industry_funding,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry"
    )

    st.plotly_chart(fig,use_container_width=True)

with col2:

    industry_valuation = (
        filtered_df.groupby("Industry")
        ["Valuation (M USD)"]
        .mean()
        .reset_index()
    )

    fig = px.pie(
        industry_valuation,
        values="Valuation (M USD)",
        names="Industry",
        title="Industry Valuation Distribution"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------------------
# Region Analysis
# ---------------------------
col1,col2 = st.columns(2)

with col1:

    region_funding = (
        filtered_df.groupby("Region")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.treemap(
        region_funding,
        path=["Region"],
        values="Funding Amount (M USD)",
        title="Regional Funding Distribution"
    )

    st.plotly_chart(fig,use_container_width=True)

with col2:

    fig = px.box(
        filtered_df,
        x="Region",
        y="Valuation (M USD)",
        title="Valuation by Region"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------------------
# Funding vs Valuation
# ---------------------------
fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Revenue (M USD)",
    hover_name="Startup Name",
    title="Funding vs Valuation"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------
# Profitability Analysis
# ---------------------------
profit_df = (
    filtered_df.groupby("Profitable")
    .size()
    .reset_index(name="Count")
)

profit_df["Profitable"] = (
    profit_df["Profitable"]
    .map({0:"No",1:"Yes"})
)

fig = px.pie(
    profit_df,
    values="Count",
    names="Profitable",
    title="Profitability Distribution"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------
# Correlation Heatmap
# ---------------------------
st.subheader("Correlation Analysis")

numeric_cols = [
    "Funding Rounds",
    "Funding Amount (M USD)",
    "Valuation (M USD)",
    "Revenue (M USD)",
    "Employees",
    "Market Share (%)"
]

corr = filtered_df[numeric_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Correlation Heatmap"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------
# Top Startups
# ---------------------------
st.subheader("Top 10 Valued Startups")

top10 = (
    filtered_df
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .head(10)
)

st.dataframe(top10)

# ---------------------------
# AI Insights
# ---------------------------
st.subheader("📊 Deep Business Insights")

highest_funding = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

highest_valuation = (
    filtered_df.groupby("Industry")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

st.success(f"""
✔ Industry receiving maximum funding: {highest_funding}

✔ Industry with highest average valuation: {highest_valuation}

✔ Overall profitability rate: {profitability_rate:.2f}%

✔ Total startup funding ecosystem value:
${total_funding:,.2f} Million
""")

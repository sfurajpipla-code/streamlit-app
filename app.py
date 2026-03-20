import streamlit as st
import polars as pl

st.set_page_config(page_title="Simple Dashboard", layout="wide")

st.title("📊 Simple Streamlit Dashboard")

# Load data (cached)
@st.cache_data
def load_data():
    df = pl.read_csv("data.csv")
    return df

df = load_data()

# Show data
st.subheader("Raw Data")
st.write(df)

# Filter
st.subheader("Filter Data")

departments = df["department"].unique().to_list()
selected_dept = st.selectbox("Select Department", ["All"] + departments)

if selected_dept != "All":
    filtered_df = df.filter(pl.col("department") == selected_dept)
else:
    filtered_df = df

st.write(filtered_df)

# Summary
st.subheader("Average Salary by Department")

summary = df.group_by("department").agg(
    pl.col("salary").mean().alias("avg_salary")
)

st.write(summary)

# Simple chart
st.subheader("Salary Chart")

chart_data = summary.to_pandas()
st.bar_chart(chart_data.set_index("department"))
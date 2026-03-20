import streamlit as st
import polars as pl

st.set_page_config(page_title="Simple Dashboard", layout="wide")
st.title("📊 Simple Streamlit Dashboard")

@st.cache_data
def load_data():
    # .strip() use karke extra spaces hatayein agar zaroorat ho
    return pl.read_csv("data.csv")

df = load_data()

# --- FILTER SECTION ---
st.subheader("Filter Data")

# Strip spaces just in case data mein kachra ho
departments = df["department"].unique().to_list()
selected_dept = st.selectbox("Select Department", ["All"] + sorted(departments))

# Filter Logic (Explicitly check)
if selected_dept != "All":
    # Yahan filtered_df create ho raha hai
    filtered_df = df.filter(pl.col("department") == selected_dept)
else:
    # All ke case mein original df
    filtered_df = df

# --- DISPLAY SECTION ---
# Dhyaan dein: Hum filtered_df display kar rahe hain
st.write(f"Displaying: {selected_dept}")
st.dataframe(filtered_df.to_pandas()) # Polars ko display ke liye pandas mein convert karna safe hai

# --- SUMMARY SECTION ---
st.subheader("Summary for Selection")

# Summary hamesha FILTERED data par honi chahiye
if not filtered_df.is_empty():
    summary = filtered_df.group_by("department").agg(
        pl.col("salary").mean().alias("avg_salary")
    )
    st.write(summary.to_pandas())
    
    # Chart bhi filtered data ka hi banega
    st.bar_chart(summary.to_pandas(), x="department", y="avg_salary")
else:
    st.warning("No data found for this selection.")

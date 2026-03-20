import streamlit as st
import polars as pl
import requests
from io import StringIO

st.set_page_config(page_title="Simple Dashboard", layout="wide")
st.title("📊 Simple Streamlit Dashboard")

Dataurl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQaVBNLvbaPYyKmt8WZ5ECI49jTuQmHO2ZVtUm0p0GpMbt3A9E6IrDgchIQx_T8kLnL4W5xp05PIO0k/pub?gid=346820640&single=true&output=csv"

@st.cache_data(ttl= 60)
def load_data(url):
    res = requests.get(url)
    csvString = res.text
    csvfile = StringIO(csvString)
    df = pl.read_csv(csvfile, infer_schema_length= 20000)
    return df

    

df = load_data(Dataurl)

st.write(f"{df.height}")

# --- FILTER SECTION ---
st.subheader("Filter Data")

# Strip spaces just in case data mein kachra ho
departments = df["RANGE"].unique().to_list()
selected_dept = st.selectbox("Select Department", ["All"] + sorted(departments))

# Filter Logic (Explicitly check)
if selected_dept != "All":
    # Yahan filtered_df create ho raha hai
    filtered_df = df.filter(pl.col("RANGE") == selected_dept)
else:
    # All ke case mein original df
    filtered_df = df

# --- DISPLAY SECTION ---
# Dhyaan dein: Hum filtered_df display kar rahe hain
st.write(f"Displaying: {selected_dept}")
st.dataframe(filtered_df) # Polars ko display ke liye pandas mein convert karna safe hai

# --- SUMMARY SECTION ---
st.subheader("Summary for Selection")

# Summary hamesha FILTERED data par honi chahiye
if not filtered_df.is_empty():
    summary = filtered_df.group_by("RANGE").agg(
        pl.col("GIRTH(CM)").mean().alias("avg_girth")
    )
    st.write(summary)
    
    # Chart bhi filtered data ka hi banega
    st.bar_chart(summary, x="RANGE", y="avg_girth")
else:
    st.warning("No data found for this selection.")

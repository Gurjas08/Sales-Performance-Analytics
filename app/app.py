import streamlit as st
import pandas as pd
from pathlib import Path

PROC_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
CSV_PATH = PROC_DIR / "sales_clean.csv"

st.set_page_config(page_title="Sales Performance", layout="wide")
st.title("📊 Sales Performance Dashboard")

@st.cache_data
def load_data():
    # InvoiceDate may already be datetime in the CSV; parse to be safe
    df = pd.read_csv(CSV_PATH, parse_dates=["InvoiceDate"])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Processed file not found. Run `python src/etl.py` first.")
    st.stop()

st.caption(f"Loaded {len(df):,} rows")

# ---- Filters ----
with st.sidebar:
    st.header("Filters")
    countries = st.multiselect("Country", sorted(df["Country"].dropna().unique().tolist()))
    months = st.multiselect("Month", sorted(df["Month"].dropna().unique().tolist()))
    include_returns = st.checkbox("Include returns (negative Quantity)", value=True)

f = df.copy()
if countries:
    f = f[f["Country"].isin(countries)]
if months:
    f = f[f["Month"].isin(months)]
if not include_returns:
    f = f[f["Quantity"] >= 0]

# ---- KPIs ----
total_rev = float(f["Revenue"].sum())
orders = f["Invoice"].nunique() if "Invoice" in f.columns else 0
customers = f["CustomerID"].nunique() if "CustomerID" in f.columns else 0
avg_basket = (total_rev / orders) if orders else 0.0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Revenue", f"${total_rev:,.0f}")
k2.metric("Orders", f"{orders:,}")
k3.metric("Avg Basket", f"${avg_basket:,.2f}")
k4.metric("Customers", f"{customers:,}")

st.divider()

# ---- Time series by Month ----
ts = (f.groupby("Month", as_index=False)["Revenue"]
        .sum().sort_values("Month"))
st.subheader("Revenue over time (by Month)")
if not ts.empty:
    st.line_chart(ts.set_index("Month"))
else:
    st.info("No data for the current filter selection.")

st.divider()

# ---- Top products ----
st.subheader("Top 15 Products by Revenue")
by_prod = (f.groupby("Description", as_index=False)["Revenue"].sum()
             .sort_values("Revenue", ascending=False).head(15))
if not by_prod.empty:
    st.bar_chart(by_prod.set_index("Description"))
    st.dataframe(by_prod, use_container_width=True)
else:
    st.info("No products match the current filters.")


# ---- Top countries ----
st.divider()
st.subheader("Top 15 Countries by Revenue")

by_country = (
    f.groupby("Country", as_index=False)["Revenue"]
     .sum()
     .sort_values("Revenue", ascending=False)
     .head(15)
)

if not by_country.empty:
    st.bar_chart(by_country.set_index("Country"))
    st.dataframe(by_country, use_container_width=True)
else:
    st.info("No countries match the current filters.")


st.divider()
st.subheader("Download filtered data")
st.download_button(
    "Download CSV",
    data=f.to_csv(index=False).encode("utf-8"),
    file_name="sales_filtered.csv",
    mime="text/csv",
)


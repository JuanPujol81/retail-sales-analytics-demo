import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Retail Sales Analytics", layout="wide")
st.title("Retail Sales Analytics — Demo")

st.markdown("""
This demo shows a simple analytics pipeline: synthetic dataset → KPIs → filters → chart.
Recruiter-friendly: runs in one click, no setup.
""")

# Synthetic dataset
rng = np.random.default_rng(7)
n = 500
df = pd.DataFrame({
    "invoice_id": np.arange(1, n+1),
    "store": rng.choice(["North","South","East","West"], size=n),
    "category": rng.choice(["A","B","C"], size=n, p=[.5,.3,.2]),
    "units": rng.integers(1, 12, size=n),
    "price": np.round(rng.normal(20, 5, size=n), 2),
})
df["revenue"] = df["units"] * df["price"]

# Sidebar filters
st.sidebar.header("Filters")
store_sel = st.sidebar.multiselect("Store", sorted(df["store"].unique()))
cat_sel = st.sidebar.multiselect("Category", sorted(df["category"].unique()))

f = df.copy()
if store_sel:
    f = f[f["store"].isin(store_sel)]
if cat_sel:
    f = f[f["category"].isin(cat_sel)]

# KPIs
total_rev = float(f["revenue"].sum())
avg_ticket = float((f["revenue"] / f["units"]).mean())
top_store = f.groupby("store")["revenue"].sum().sort_values(ascending=False).head(1)

c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue (€)", f"{total_rev:,.2f}")
c2.metric("Avg Ticket (€)", f"{avg_ticket:,.2f}")
c3.metric("Top Store", top_store.index[0] if len(top_store)>0 else "—")

# Chart
rev_by_cat = f.groupby("category")["revenue"].sum().sort_values(ascending=False)
st.subheader("Revenue by Category")
st.bar_chart(rev_by_cat)

st.caption("Synthetic data for demo purposes. Built with Streamlit.")

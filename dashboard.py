import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "bookmakers.db"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM bookmakers", conn)
    conn.close()
    return df

st.set_page_config(page_title="Bookmaker Intelligence Dashboard", layout="wide")
st.title("Bookmaker Intelligence Dashboard")

df = load_data()

with st.expander("Show Raw Data Table"):
    st.dataframe(df)

st.subheader("Number of Bookmakers by Country")
country_counts = df['country'].value_counts()
st.bar_chart(country_counts)

st.subheader("Product Offering Distribution")
all_products = df['products'].dropna().str.split(', ')
flat_products = [item for sublist in all_products for item in sublist]
product_counts = pd.Series(flat_products).value_counts()

fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    product_counts,
    labels=product_counts.index,
    autopct='%1.1f%%',
    textprops={'color': 'white'}
)

ax.set_ylabel("")

st.plotly_chart(fig, use_container_width=True)

st.subheader("Licensing Authorities")
licensing = df['licensing'].dropna().str.split(', ')
flat_licenses = [item for sublist in licensing for item in sublist]
licensing_counts = pd.Series(flat_licenses).value_counts()
st.bar_chart(licensing_counts)
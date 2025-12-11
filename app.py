import streamlit as st
import pandas as pd
import numpy as np


# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(layout="wide")
st.title("Inventory Management App")


# ---------------------------
# Session Sate
# ---------------------------

if "df" not in st.session_state:
    st.session_state.df = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "selected_time" not in st.session_state:
    st.session_state.selected_item = None

# Header container
with st.container():
    # Input CSV
    if st.session_state.df is None:
        stock_csv = st.file_uploader("Import This Month's Stock (.csv)", type="csv")
        if stock_csv is not None:
            st.session_state.df = pd.read_csv(stock_csv)
            st.session_state.file_name = stock_csv.name
    if st.session_state.df is not None:
        st.success(f"Successfully Uploaded File: {st.session_state.file_name}")
        st.toast("Successfully Uploaded!", icon="✅", duration=1)

st.divider()

stock_col, plot_col = st.columns([1,2], gap="medium")
df = st.session_state.df

with stock_col:
    st.subheader("Current Month's Inventory")
    if df is None:
        st.warning("You need to upload this month's (.csv) file.")
    else:
        with st.container(border=True, height=750):
            for _, row in df.iterrows():
                p_id = row["id"]
                p_name = row["product_name"]
                with st.container(horizontal=True, border=True):
                    c1, c2, c3, c4 = st.columns([2, 1, 2, 1])
                with c1:
                    st.write(f"#### {p_name}")
                    st.caption(f"ID: {p_id}")

                with c2:

                    st.metric("Inventory", row["inventory"])

                with c3:
                    st.write(row["supplier_name"])
                    st.caption("Supplier")
                with c4:
                    if st.button("Select", key=f"select_{p_name}"):
                        st.session_state.selected_item = p_name


with plot_col:
    st.subheader("Item Sale's Plot")
    if df is None:
        st.warning("You need to upload this month's (.csv) file.")
    else:
        product_list = df["product_name"].tolist()

        default_index = (
            product_list.index(st.session_state.selected_item) if st.session_state.selected_item in product_list
            else 0
        )

        st.session_state.selected_item = st.selectbox("Choose A Product",product_list, index=default_index)
        st.write(st.session_state.selected_item)
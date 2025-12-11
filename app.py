import streamlit as st
import pandas as pd
import numpy as np


# ---------------------------
# Page Config
# ---------------------------
st.title("Inventory Management App")


# ---------------------------
# Session Sate200
# ---------------------------

if "df1" not in st.session_state:
    st.session_state.df1 = None

if "df2" not in st.session_state:
    st.session_state.df2 = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "sales_name" not in st.session_state:
    st.session_state.sales_name = None

if "selected_time" not in st.session_state:
    st.session_state.selected_item = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

with st.sidebar:
    st.sidebar.title("Navigation")
    if st.button("Home"):
        st.session_state.page = "Home"
    if st.button("View Inventory"):
        st.session_state.page = "Inventory"
    if st.button("How to Use?"):
        st.session_state.page = "HowToUse"

# ---------------------------
# Inputting CSV
# ---------------------------
def home_page():
    success = 0
    st.write("## Home Page")
    with st.container():
        # Input CSV
        if st.session_state.df1 is None:
            stock_csv = st.file_uploader("Import This Month's Stock (.csv)", type="csv")
            if stock_csv is not None:
                st.session_state.df1 = pd.read_csv(stock_csv)
                st.session_state.file_name = stock_csv.name

        if st.session_state.df2 is None:
            sales_csv = st.file_uploader("Import This Month's Sales (.csv)", type="csv")
            if sales_csv is not None:
                st.session_state.df2 = pd.read_csv(sales_csv)
                st.session_state.sales_name = sales_csv.name
            

        if st.session_state.df1 is not None:
            st.success(f"Successfully Uploaded File: {st.session_state.file_name}")
            st.toast("Successfully Uploaded!", icon="✅", duration=1)
            success += 1
        if st.session_state.df2 is not None:
            st.success(f"Successfully Uploaded File: {st.session_state.sales_name}")
            st.toast("Successfully Uploaded!", icon="✅", duration=1)
            success += 1

        if success == 2:
            st.set_page_config(layout="wide")

    st.divider()

    # ---------------------------
    # Showing Data
    # ---------------------------


    stock_col, plot_col = st.columns([1,1], gap="medium")
    df1 = st.session_state.df1

    with stock_col.container(border=True, height=1000):
        st.title("Current Month's Inventory")
        if df1 is None:
            st.warning("You need to upload this month's (.csv) file.")
        else:
            with st.container(border=True):
                pred_value = 200
                for _, row in df1.iterrows():
                    p_id = row["id"]
                    p_name = row["product_name"]
                    curr_stock = row["inventory"]
                    with st.container(horizontal=True, border=True):
                        c_name, c_currstock, c_pred, c_suppname, c_button = st.columns([1, 1, 1, 1, 1])
                    with c_name:
                        st.write(f"#### {p_name}")
                        st.caption(f"ID: {p_id}")

                    with c_currstock:
                        diff = (curr_stock - pred_value)
                        st.metric("Inventory", curr_stock, diff )
                    with c_pred:
                        st.metric("Prediction", pred_value)
                    with c_suppname:
                        st.write(row["supplier_name"])
                        st.caption("Supplier")
                    with c_button:
                        if st.button("Select", key=f"select_{p_name}"):
                            st.session_state.selected_item = p_name


    with plot_col.container(border=True, height=1000):
        st.title("Item Sale's Plot")
        if df1 is None:
            st.warning("You need to upload this month's (.csv) file.")
        else:
            product_list = df1["product_name"].tolist()

            default_index = (
                product_list.index(st.session_state.selected_item) if st.session_state.selected_item in product_list
                else 0
            )

            st.session_state.selected_item = st.selectbox("Choose A Product",product_list, index=default_index)
            st.write(st.session_state.selected_item)

    st.divider()
    # ---------------------------
    # Export CSV
    # ---------------------------
    st.title("Export to CSV")


def inventory_page():
    st.write("## Raw CSV")
    df1 = st.session_state.df1
    df2 = st.session_state.df2
    if df1 is not None:
        st.success(f"Successfully Uploaded File: {st.session_state.file_name}")
        st.write(df1)
    else:
        st.warning("No CSV uploaded yet!")
    if df2 is not None:
        st.success(f"Successfully Uploaded File: {st.session_state.sales_name}")
        st.write(df2)
    else:
        st.warning("No CSV uploaded yet!")


def how_page():
    st.write("## gay nigger")


# ---------------------------
# Page Router
# ---------------------------

page = st.session_state.page

if page == "Home":
    home_page()

if page == "Inventory":
    inventory_page()

if page == "HowToUse":
    how_page()
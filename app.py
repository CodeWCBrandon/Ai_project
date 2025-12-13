import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from prophet import Prophet


# ---------------------------
# Dummy Model
# ---------------------------

class DummySalesModel:
    def predict(self, X):
        base = X[:, 0]          # current sales
        noise = np.random.normal(0, 2, size=len(X))
        return base * 0.8 + noise
    
# ---------------------------
# Predictive AI (Prophet)
# ---------------------------

def get_prediction(df):
    data = df.copy()
    # normalize column names (strip spaces)
    data.columns = data.columns.str.strip()

    # ensure types
    data['Item Code'] = data['Item Code'].astype('string')
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Quantity Sold (kilo)'] = pd.to_numeric(data['Quantity Sold (kilo)'], errors='coerce')

    forecast_list_result = []
    for unique_code in data['Item Code'].unique():
        item_data = data[data['Item Code'] == unique_code].copy()

        # aggregate by date
        item_data = item_data.groupby('Date', as_index=False)['Quantity Sold (kilo)'].sum()

        # drop invalid dates / negative or NaN y
        item_data = item_data[item_data['Date'].notna()]
        item_data = item_data[item_data['Quantity Sold (kilo)'].notna() & (item_data['Quantity Sold (kilo)'] >= 0)]

        if item_data.shape[0] < 2:
            print(f"Not enough data for {unique_code}, skipping.")
            continue

        item_data = item_data.rename(columns={'Date': 'ds', 'Quantity Sold (kilo)': 'y'})

        product_name = (
            data.loc[data['Item Code'] == unique_code, 'product_name']
            .iloc[0]
        )

        # initialize and fit
        model = Prophet(yearly_seasonality=False, changepoint_prior_scale=0.001)
        model.add_seasonality(name='yearly', period=365.25, fourier_order=9)
        model.add_seasonality(name='weekly', period=7, fourier_order=3)
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)

        model.fit(item_data)        # pass the DataFrame directly

        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        forecast['Item Code'] = unique_code
        forecast['product_name'] = product_name
        forecast_list_result.append(forecast[['Item Code', 'product_name', 'ds', 'yhat', 'yhat_lower', 'yhat_upper']])
    return forecast_list_result




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

if "forecasts" not in st.session_state:
    st.session_state.forecasts = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "sales_name" not in st.session_state:
    st.session_state.sales_name = None

if "selected_time" not in st.session_state:
    st.session_state.selected_item = None

if "df2_pred" not in st.session_state:
    st.session_state.df2_pred = None

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
# Importing Model
# ---------------------------
dummy_model = DummySalesModel()

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
                st.session_state.df1 = pd.read_csv(stock_csv,)
                st.session_state.file_name = stock_csv.name

        if st.session_state.df2 is None:
            sales_csv = st.file_uploader("Import This Month's Sales (.csv)", type="csv")
            if sales_csv is not None:
                st.session_state.df2 = pd.read_csv(sales_csv, parse_dates=["Date"])
                st.session_state.sales_name = sales_csv.name

                # Real Forecast
                forecasts = get_prediction(st.session_state.df2)
                st.session_state.forecasts = pd.concat(forecasts, ignore_index=True)

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
    df2 = st.session_state.df2
    forecasts = st.session_state.forecasts

    with stock_col.container(border=True, height=1000):
        st.title("Current Month's Inventory")
        if df1 is None:
            st.warning("You need to upload this month's (.csv) file.")
        else:
            with st.container(border=True):
                for _, row in df1.iterrows():
                    p_id = str(row["Item Code"]).strip()
                    p_name = row["product_name"]
                    curr_stock = row["inventory"]
                    
                    item_forecast = forecasts[forecasts["Item Code"].astype(str).str.strip() == p_id]
                    if item_forecast.empty:
                        pred_value = 76
                    else:
                        future_pred = item_forecast.tail(30)
                        pred_value = int(future_pred["yhat"].sum())

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


    with plot_col.container(border=True):
        st.title("Item Sale's Plot")
        if df2 is None:
            st.warning("You need to upload this month's (.csv) file.")
        else:
            product_list = df2["product_name"].unique().tolist()

            default_index = (
                product_list.index(st.session_state.selected_item) if st.session_state.selected_item in product_list
                else 0
            )

            st.session_state.selected_item = st.selectbox("Choose A Product",product_list, index=default_index)
            df2_plot = df2[df2["product_name"] == st.session_state.selected_item].copy()
            df2_plot = df2_plot.sort_values("Date")
            df2_pred_plot = forecasts[forecasts["product_name"] == st.session_state.selected_item].copy()
            df2_pred_plot = df2_pred_plot.sort_values("Date")
            # Real Sales Plot
            if (not df2_plot.empty) and {"Date", "sales"}.issubset(df2_plot.columns):
                fig = go.Figure() 

                # Sales trace
                fig.add_trace(
                    go.Scatter(
                        x=df2_plot["Date"],
                        y=df2_plot["sales"],
                        mode="lines+markers",
                        name=f"{st.session_state.selected_item} Sales"
                    )
                )

                # Styling
                fig.update_layout(
                    title=f"Daily Sales for {st.session_state.selected_item}",
                    xaxis=dict(title="Date"),
                    yaxis=dict(title="Sales (units)"),
                    height=520,
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.3,
                        xanchor="center",
                        x=0.5,
                    )
                )
                # st.plotly_chart(fig, use_container_width=True)
            # Predicted Sales Plot
            if (not df2_pred_plot.empty) and {"Date", "p_sales"}.issubset(df2_pred_plot.columns):
                pred_fig = go.Figure()

                # compare to Real
                fig.add_trace(
                    go.Scatter(
                        x=df2_pred_plot["Date"],
                        y=df2_pred_plot["sales"],
                        mode="lines+markers",
                        name=f"{st.session_state.selected_item} Predicted Sales"
                    )
                )

                 # Predicted Sales trace
                pred_fig.add_trace(
                    go.Scatter(
                        x=df2_pred_plot["Date"],
                        y=df2_pred_plot["p_sales"],
                        mode="lines+markers",
                        name=f"{st.session_state.selected_item} Sales"
                    )
                )

                # Styling
                fig.update_layout(
                    title=f"Daily Prediction Sales for {st.session_state.selected_item}",
                    xaxis=dict(title="Date"),
                    yaxis=dict(title="Sales (units)"),
                    height=520
                )
                st.plotly_chart(fig, use_container_width=True)
            
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


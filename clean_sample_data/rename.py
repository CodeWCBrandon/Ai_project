import pandas as pd

# load files
data1 = pd.read_csv("sample/filtered_sales.csv")
data2 = pd.read_csv("sample/filtered_items.csv")

# normalize column names (important)
data1.columns = data1.columns.str.strip()
data2.columns = data2.columns.str.strip()

# ensure Item Code matches type
data1["Item Code"] = data1["Item Code"].astype(str).str.strip()
data2["Item Code"] = data2["Item Code"].astype(str).str.strip()

# keep only what we need from data2
data2 = data2.rename(columns={"Item Name": "product_name"})[
    ["Item Code", "product_name"]
]

# merge (LEFT JOIN: keep all sales rows)
merged = data1.merge(
    data2,
    on="Item Code",
    how="left"
)

# optional: reorder columns
cols = [
    "Date",
    "Time",
    "Item Code",
    "product_name",
    "Quantity Sold (kilo)",
    "Unit Selling Price (RMB/kg)",
    "Sale or Return",
    "Discount (Yes/No)"
]
merged = merged[cols]

# save result
merged.to_csv("annex2_with_product_name.csv", index=False)

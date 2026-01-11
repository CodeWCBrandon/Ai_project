import pandas as pd
import random

# load full item list
df_items = pd.read_csv("annex1.csv")

# supplier pool
suppliers = [
    "GreenLeaf Supplier",
    "FreshFarm Co",
    "Daily Greens Ltd",
    "Urban Veggie Supply",
    "PackFresh Logistics",
    "Fungi World",
    "Capsicum Traders",
    "Solanum Growers"
]

# generate inventory (category-aware if you want)
def generate_inventory(category):
    if "Leaf" in category or "Vegetables" in category:
        return random.randint(60, 180)
    if "Mushroom" in category:
        return random.randint(40, 160)
    if "Capsicum" in category:
        return random.randint(30, 100)
    if "Solanum" in category:
        return random.randint(40, 120)
    return random.randint(50, 150)

# create stock dataframe
stock_df = pd.DataFrame({
    "Item Code": df_items["Item Code"].astype(str),
    "product_name": df_items["Item Name"],
    "inventory": df_items["Category Name"].apply(generate_inventory),
    "supplier_name": random.choices(suppliers, k=len(df_items))
})

# save
stock_df.to_csv("stock.csv", index=False)

import pandas as pd
import random

# Read your filtered items CSV
items_df = pd.read_csv("sample/filtered_items.csv")

# Rename Item Name to product_name
items_df = items_df.rename(columns={"Item Name": "product_name"})

# Keep only Item Code and product_name
items_df = items_df[["Item Code", "product_name"]]

# Add random inventory (e.g., 50 to 500 units)
items_df["inventory"] = [random.randint(50, 500) for _ in range(len(items_df))]

# Add random supplier name from a sample list
supplier_list = ["Supplier A", "Supplier B", "Supplier C", "Supplier D"]
items_df["supplier_name"] = [random.choice(supplier_list) for _ in range(len(items_df))]

# Save to new CSV
items_df.to_csv("items_with_inventory.csv", index=False)

print("New items CSV with random inventory and suppliers created:", len(items_df), "rows")

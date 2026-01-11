import pandas as pd

# Path to your items CSV
items_file = "annex1.csv"

# List of target Item Codes
target_items = [
    "102900005115878",  # example Item Codes
    "102900005115793",
    "102900011000632",
    # "102900005115823",
    # "102900011006689",
    "102900011009444",
    "102900011000335",
    # "102900051004294",
    # "102900011030608"
]

# Read items CSV
items_df = pd.read_csv(items_file)

# Filter only the target items
filtered_items_df = items_df[items_df["Item Code"].astype(str).isin(target_items)]

# Save to a new CSV
filtered_items_df.to_csv("filtered_items.csv", index=False)

print("Filtered items CSV saved with", len(filtered_items_df), "rows")

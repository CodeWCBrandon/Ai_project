import pandas as pd

# Path to your large CSV
file_path = "annex2.csv"

# List of Item Codes (or product_names) you want to keep
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
    # add up to ~10 items you care about
]

# Prepare an empty dataframe
filtered_df = pd.DataFrame()

# Read CSV in chunks
chunksize = 100_000  # adjust as needed
for chunk in pd.read_csv(file_path, chunksize=chunksize):
    chunk_filtered = chunk[chunk["Item Code"].astype(str).isin(target_items)]
    filtered_df = pd.concat([filtered_df, chunk_filtered], ignore_index=True)

# Optional: sort by Date
filtered_df = filtered_df.sort_values(["Item Code", "Date"])

# Save to a smaller CSV
filtered_df.to_csv("filtered_sales.csv", index=False)

print("Filtered CSV saved with", len(filtered_df), "rows")

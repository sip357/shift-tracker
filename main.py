import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ----------------------------
# Read Excel Sheets
# ----------------------------

file_path = "data/shift_data.xlsx"

plan_df = pd.read_excel(file_path, sheet_name="Plan")
actual_df = pd.read_excel(file_path, sheet_name="Actual")

# ----------------------------
# Merge Data
# ----------------------------

merged_df = pd.merge(
    plan_df,
    actual_df,
    on=["Date", "Shift", "Zone"],
    how="inner"
)

# ----------------------------
# Calculate Variance
# ----------------------------

merged_df["Variance"] = (
    merged_df["Actual_Tonnes"]
    - merged_df["Planned_Tonnes"]
)

print(merged_df)

# ----------------------------
# Save to SQLite
# ----------------------------

conn = sqlite3.connect("output/shift_tracker.db")

merged_df.to_sql(
    "shift_variance",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Data saved to SQLite database.")

# ----------------------------
# Create Bar Chart
# ----------------------------

zone_variance = merged_df.groupby("Zone")["Variance"].sum()

plt.figure(figsize=(8, 5))
zone_variance.plot(kind="bar")

plt.title("Variance by Zone")
plt.xlabel("Zone")
plt.ylabel("Variance (Actual - Planned)")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("output/variance_chart.png")

print("Chart saved.")
"""
WEEK 3 - DATA VISUALIZATION AND REPORTING
Dataset: Sample - Superstore.csv

Required visuals:
1. Bar chart
2. Line chart
3. Scatter plot
4. Heatmap

Additional:
5. Sub-category profit
6. Discount vs profit
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "Sample - Superstore.csv"
OUTPUT_DIR = BASE_DIR / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {INPUT_FILE}\n"
        "Place 'Sample - Superstore.csv' in the same folder as this script."
    )

df = pd.read_csv(INPUT_FILE, encoding="latin1")
df.columns = df.columns.str.strip()

for col in ["Order Date", "Ship Date"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

for col in ["Sales", "Quantity", "Discount", "Profit", "Postal Code"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.drop_duplicates().copy()
df["Profit Margin"] = np.where(df["Sales"] != 0, df["Profit"] / df["Sales"], np.nan)
df["Order Year"] = df["Order Date"].dt.year

print("Shape:", df.shape)
print("Missing cells:", int(df.isna().sum().sum()))
print("Duplicate rows:", int(df.duplicated().sum()))
print("Total sales:", round(df["Sales"].sum(), 2))
print("Total profit:", round(df["Profit"].sum(), 2))

# 1. Bar chart
category_summary = (
    df.groupby("Category")[["Sales", "Profit"]]
      .sum()
      .sort_values("Sales", ascending=False)
)

ax = category_summary.plot(kind="bar", figsize=(9, 5.2))
ax.set_title("Sales and Profit by Product Category")
ax.set_xlabel("Category")
ax.set_ylabel("Amount (USD)")
ax.grid(axis="y", alpha=0.25)
ax.legend(title="")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_category_sales_profit_bar.png", dpi=180, bbox_inches="tight")
plt.close()

# 2. Line chart
annual_sales = df.groupby("Order Year")["Sales"].sum()
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.plot(annual_sales.index, annual_sales.values, marker="o", linewidth=2)
for year, sales in annual_sales.items():
    ax.annotate(f"${sales/1000:.0f}K", (year, sales),
                textcoords="offset points", xytext=(0, 8), ha="center")
ax.set_title("Annual Sales Trend")
ax.set_xlabel("Year")
ax.set_ylabel("Sales (USD)")
ax.grid(True, alpha=0.25)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_annual_sales_line.png", dpi=180, bbox_inches="tight")
plt.close()

# 3. Scatter plot
region_summary = df.groupby("Region")[["Sales", "Profit"]].sum()
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.scatter(region_summary["Sales"], region_summary["Profit"], s=120)
for region, row in region_summary.iterrows():
    ax.annotate(region, (row["Sales"], row["Profit"]),
                textcoords="offset points", xytext=(7, 6))
ax.set_title("Regional Sales vs Profit")
ax.set_xlabel("Sales (USD)")
ax.set_ylabel("Profit (USD)")
ax.grid(True, alpha=0.25)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_regional_sales_profit_scatter.png", dpi=180, bbox_inches="tight")
plt.close()

# 4. Heatmap
heatmap_data = df.pivot_table(
    index="Region",
    columns="Category",
    values="Profit",
    aggfunc="sum"
)
fig, ax = plt.subplots(figsize=(8.5, 5.5))
im = ax.imshow(heatmap_data.values, aspect="auto")
ax.set_title("Profit Heatmap: Region × Category")
ax.set_xticks(np.arange(heatmap_data.shape[1]))
ax.set_xticklabels(heatmap_data.columns, rotation=15)
ax.set_yticks(np.arange(heatmap_data.shape[0]))
ax.set_yticklabels(heatmap_data.index)
for i in range(heatmap_data.shape[0]):
    for j in range(heatmap_data.shape[1]):
        ax.text(j, i, f"${heatmap_data.iloc[i,j]/1000:.1f}K",
                ha="center", va="center", fontsize=9)
fig.colorbar(im, ax=ax, label="Profit (USD)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_profit_region_category_heatmap.png", dpi=180, bbox_inches="tight")
plt.close()

# 5. Additional: sub-category profit
subcat_summary = df.groupby("Sub-Category")["Profit"].sum().sort_values()
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(subcat_summary.index, subcat_summary.values)
ax.axvline(0, linewidth=1)
ax.set_title("Profit by Sub-Category")
ax.set_xlabel("Profit (USD)")
ax.set_ylabel("Sub-Category")
ax.grid(axis="x", alpha=0.25)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_subcategory_profit.png", dpi=180, bbox_inches="tight")
plt.close()

# 6. Additional: discount vs profit
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.scatter(df["Discount"], df["Profit"], alpha=0.25, s=16)
ax.axhline(0, linewidth=1)
ax.set_title("Discount vs Profit")
ax.set_xlabel("Discount Rate")
ax.set_ylabel("Profit (USD)")
ax.grid(True, alpha=0.25)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "06_discount_vs_profit_scatter.png", dpi=180, bbox_inches="tight")
plt.close()

print("All Week 3 visualizations generated successfully.")

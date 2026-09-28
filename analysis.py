"""Sales Performance Analysis
Analyses sales data to find top regions, products and monthly trends.
Run: python analysis.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA_FILE = "sales_data.csv"


def make_sample_data(path, rows=500, seed=42):
    """Creates SAMPLE data so the project runs anywhere. Replace with real data."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "date": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, rows), unit="D"),
        "region": rng.choice(["North", "South", "East", "West"], rows, p=[0.2, 0.35, 0.2, 0.25]),
        "product": rng.choice(["Basic Plan", "Pro Plan", "Enterprise Plan"], rows, p=[0.5, 0.3, 0.2]),
        "customer": [f"Customer_{i}" for i in rng.integers(1, 80, rows)],
        "units": rng.integers(1, 10, rows),
    })
    price = {"Basic Plan": 500, "Pro Plan": 1500, "Enterprise Plan": 5000}
    df["revenue"] = df["units"] * df["product"].map(price)
    df.sort_values("date").to_csv(path, index=False)


def main():
    if not os.path.exists(DATA_FILE):
        make_sample_data(DATA_FILE)
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)

    by_region = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    by_product = df.groupby("product")["revenue"].sum().sort_values(ascending=False)
    monthly = df.groupby("month")["revenue"].sum()
    top_customers = df.groupby("customer")["revenue"].sum().nlargest(5)

    print("=== SALES SUMMARY ===")
    print(f"Total revenue : Rs {df['revenue'].sum():,}")
    print(f"Total orders  : {len(df)}")
    print(f"Avg order     : Rs {df['revenue'].mean():,.0f}")
    print(f"\nBest region   : {by_region.index[0]} (Rs {by_region.iloc[0]:,})")
    print(f"Best product  : {by_product.index[0]} (Rs {by_product.iloc[0]:,})")
    print(f"Best month    : {monthly.idxmax()} (Rs {monthly.max():,})")
    print("\nTop 5 customers:")
    print(top_customers.to_string())

    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    by_region.plot(kind="bar", ax=ax[0], color="#1F3A5F", title="Revenue by Region")
    by_product.plot(kind="bar", ax=ax[1], color="#2A9D8F", title="Revenue by Product")
    monthly.plot(ax=ax[2], marker="o", color="#E9C46A", title="Monthly Revenue")
    for a in ax:
        a.set_xlabel("")
        a.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.savefig("sales_charts.png", dpi=120)
    print("\nCharts saved to sales_charts.png")


if __name__ == "__main__":
    main()

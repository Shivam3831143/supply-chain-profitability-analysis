
from pathlib import Path
import numpy as np
import pandas as pd

# Save demo dataset in deployment folder
OUTPUT_PATH = Path(__file__).resolve().parent / "demo_dataset.csv"

np.random.seed(42)
rows = 5000

products = [
    "Laptop", "Smartphone", "Headphones", "Keyboard",
    "Monitor", "Mouse", "Tablet", "Printer"
]

segments = ["Consumer", "Corporate", "Home Office"]
markets = ["Africa", "Europe", "LATAM", "Pacific Asia", "USCA"]
regions = ["North", "South", "East", "West"]
categories = ["Technology", "Furniture", "Office Supplies"]
statuses = ["COMPLETE", "PENDING", "CLOSED", "PROCESSING"]

df = pd.DataFrame({
    "Order Id": np.arange(100001, 100001 + rows),

    # Customer information
    "Customer Id": np.random.randint(1000, 3000, rows),
    "Order Customer Id": np.random.randint(1000, 3000, rows),
    "Customer Segment": np.random.choice(segments, rows),

    # Market and product information
    "Market": np.random.choice(markets, rows),
    "Order Region": np.random.choice(regions, rows),
    "Category Name": np.random.choice(categories, rows),
    "Product Name": np.random.choice(products, rows),

    # Order and financial information
    "Order Item Quantity": np.random.randint(1, 6, rows),
    "Order Item Product Price": np.random.uniform(20, 1000, rows).round(2),
    "Order Item Discount": np.random.uniform(0, 100, rows).round(2),
    "Order Item Discount Rate": np.random.uniform(0, 0.3, rows).round(2),
    "Order Item Total": np.random.uniform(20, 2000, rows).round(2),
    "Benefit per order": np.random.uniform(-100, 300, rows).round(2),
    "Sales": np.random.uniform(20, 2000, rows).round(2),

    # Shipping and order status
    "Order Status": np.random.choice(statuses, rows),
    "Days for shipping (real)": np.random.randint(1, 10, rows),
    "Days for shipment (scheduled)": np.random.randint(1, 8, rows),
})

# Generate CSV file
df.to_csv(OUTPUT_PATH, index=False)

print("Demo dataset created successfully!")
print(f"File location: {OUTPUT_PATH}")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print("\nAvailable columns:")
print(df.columns.tolist())

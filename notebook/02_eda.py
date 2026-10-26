import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(**file**).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Use the cleaned dataset if available; otherwise use the original.

cleaned_file = DATA_DIR / "cleaned_ecommerce.csv"
original_file = DATA_DIR / "ecommerce.csv"

if cleaned_file.exists():
df = pd.read_csv(cleaned_file)
elif original_file.exists():
df = pd.read_csv(original_file)
else:
raise FileNotFoundError(
"Dataset not found. Add ecommerce.csv to the data folder."
)

print("\n--- Dataset Overview ---")
print("Shape:", df.shape)

print("\n--- First Five Rows ---")
print(df.head())

print("\n--- Dataset Information ---")
df.info()

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Statistical Summary ---")
print(df.describe(include="all"))

print("\n--- Duplicate Rows ---")
print(df.duplicated().sum())

# Plot numerical columns when available.

numeric_columns = df.select_dtypes(include="number").columns

if len(numeric_columns) > 0:
df[numeric_columns].hist(figsize=(12, 8))
plt.tight_layout()

```
output_file = BASE_DIR / "eda_distributions.png"
plt.savefig(output_file)
plt.close()

print(f"\nDistribution plots saved to: {output_file}")
```

print("\nEDA completed successfully!")

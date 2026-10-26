import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

input_file = DATA_DIR / "ecommerce.csv"
output_file = DATA_DIR / "cleaned_ecommerce.csv"

if not input_file.exists():
    print("Dataset not found. Please upload ecommerce.csv into the data folder.")
else:
    df = pd.read_csv(input_file)

    df.drop_duplicates(inplace=True)
    df.dropna(how="all", inplace=True)

    df.to_csv(output_file, index=False)

    print("Data cleaning completed successfully!")

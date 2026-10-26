import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
page_title="RetailPulse Analytics",
page_icon="📊",
layout="wide"
)

st.title("RetailPulse: E-commerce Analytics")
st.write("Analyze sales, revenue, products, and customer purchasing patterns.")

uploaded_file = st.file_uploader(
"Upload your e-commerce CSV dataset",
type=["csv"]
)

if uploaded_file is None:
st.info("Upload your CSV file to start analyzing your e-commerce data.")
st.stop()

try:
df = pd.read_csv(uploaded_file)
except Exception as e:
st.error(f"Unable to read the CSV file: {e}")
st.stop()

if df.empty:
st.error("The uploaded dataset is empty.")
st.stop()

df.columns = df.columns.str.strip()

st.success("Dataset loaded successfully!")

st.subheader("Dataset Preview")
st.dataframe(df.head(20), use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
st.metric("Total Records", f"{len(df):,}")

with col2:
st.metric("Total Columns", len(df.columns))

with col3:
st.metric(
"Duplicate Rows",
f"{df.duplicated().sum():,}"
)

st.subheader("Data Quality")
quality = pd.DataFrame({
"Missing Values": df.isnull().sum(),
"Missing Percentage": (
df.isnull().mean() * 100
).round(2)
})
st.dataframe(quality, use_container_width=True)

numeric_cols = df.select_dtypes(include="number").columns.tolist()

if numeric_cols:
st.subheader("Numerical Analysis")

```
selected_column = st.selectbox(
    "Choose a numerical column",
    numeric_cols
)

fig = px.histogram(
    df,
    x=selected_column,
    title=f"Distribution of {selected_column}"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Statistical Summary")
st.dataframe(df[numeric_cols].describe(), use_container_width=True)
```

categorical_cols = df.select_dtypes(
include=["object", "category"]
).columns.tolist()

if categorical_cols:
st.subheader("Category Analysis")

```
selected_category = st.selectbox(
    "Choose a category column",
    categorical_cols
)

category_counts = (
    df[selected_category]
    .fillna("Missing")
    .astype(str)
    .value_counts()
    .head(15)
    .reset_index()
)

category_counts.columns = ["Category", "Count"]

fig = px.bar(
    category_counts,
    x="Category",
    y="Count",
    title=f"Top Categories: {selected_category}"
)
st.plotly_chart(fig, use_container_width=True)
```

st.subheader("Download Cleaned Dataset")

cleaned_df = df.drop_duplicates().dropna(how="all")

st.download_button(
label="Download Cleaned CSV",
data=cleaned_df.to_csv(index=False).encode("utf-8"),
file_name="cleaned_ecommerce.csv",
mime="text/csv"
)

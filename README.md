# 📊 RetailPulse AI — E-Commerce Sales & Customer Intelligence Dashboard

An end-to-end **Data Analytics and Business Intelligence project** that transforms e-commerce transaction data into actionable business insights using Python, SQL, Pandas, and Streamlit.

## 🎯 Project Overview

RetailPulse AI helps businesses understand sales performance, customer purchasing behavior, product profitability, and customer satisfaction through an interactive analytics dashboard.

The project demonstrates practical data analytics skills, including data cleaning, exploratory data analysis, SQL querying, KPI development, and customer segmentation.

## 🚀 Key Features

* **Sales Analytics:** Track revenue, orders, and average order value.
* **Customer Intelligence:** Analyze purchasing frequency and customer behavior.
* **Product Analysis:** Compare category-level sales performance.
* **Geographic Analysis:** Explore sales across different states.
* **Customer Reviews:** Examine customer feedback and satisfaction.
* **Interactive Dashboard:** Filter data and explore trends dynamically.
* **Data Export:** Download filtered data as CSV.
* **RFM Segmentation:** Categorize customers based on recency, frequency, and monetary value.

## 🛠️ Tech Stack

* **Programming:** Python
* **Data Analysis:** Pandas, NumPy
* **Visualization:** Plotly
* **Dashboard:** Streamlit
* **Database & Queries:** SQL, SQLite
* **Business Intelligence:** Power BI, DAX
* **Version Control:** Git and GitHub

## 📂 Project Structure

```text
RetailPulse-Ecommerce-Analytics/
│
├── app.py
├── requirements.txt
├── README.md
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_customer_segmentation.ipynb
│   └── 04_load_sqlite.ipynb
├── sql/
│   └── analysis_queries.sql
├── dashboard/
│   └── dax_measures.txt
├── data/
│   ├── raw/
│   └── cleaned/
└── STEPS.md
```

## 📈 Business Questions Addressed

1. How does revenue change over time?
2. Which product categories perform best?
3. Which geographic regions generate the most sales?
4. How frequently do customers make purchases?
5. What patterns appear in customer reviews?
6. Which customers may require targeted retention campaigns?
7. How can businesses use purchasing patterns to improve decisions?

## 📊 Dataset

The project can use the publicly available **Brazilian E-Commerce Public Dataset by Olist**.

Dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The dataset contains information about orders, customers, products, payments, sellers, and customer reviews.

Download the dataset separately and follow the project instructions to prepare the data before performing real-data analysis.

The application can also run using demo data when the real dataset is unavailable.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/RetailPulse-Ecommerce-Analytics.git
```

### 2. Open the project directory

```bash
cd RetailPulse-Ecommerce-Analytics
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the dashboard.

## 🌐 Deployment

The dashboard can be deployed using Streamlit Community Cloud.

1. Push the project to GitHub.
2. Open https://share.streamlit.io/
3. Connect your GitHub repository.
4. Select `app.py` as the main file.
5. Deploy the application.

## 💡 Skills Demonstrated

* Data cleaning and preprocessing
* Exploratory data analysis (EDA)
* SQL queries, joins, and aggregations
* Business KPI development
* Interactive dashboard development
* Customer segmentation using RFM analysis
* Data visualization and interpretation
* Business reporting and analytical problem-solving

## 🔮 Future Enhancements

* Add customer churn prediction.
* Implement advanced customer segmentation using K-means clustering.
* Integrate automated data refresh.
* Add profit-margin and discount-effectiveness analysis where the required data is available.
* Develop a Power BI executive dashboard.
* Add sales forecasting and trend analysis.

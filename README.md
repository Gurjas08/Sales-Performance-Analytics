# 🧾 Sales Performance Analytics

**Personal Data Analytics Project**  
End-to-end workflow demonstrating:
- Automated ETL in Python (pandas)
- Data cleaning and transformation
- Interactive Streamlit dashboard for insights
- Based on a public retail dataset (~1M transactions)

---

## 📦 Dataset

We use the **Online Retail II (UCI)** dataset from Kaggle:  
👉 [Download here](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci)

### Steps to prepare the data
1. Download the dataset from Kaggle.
2. Extract it if it comes in a ZIP.
3. Find the main `.csv` file (example: `online_retail_II.csv`).
4. Place that file inside the `data/raw/` folder of this project.

---

## ⚙️ Setup Instructions

### Step 1 — Install dependencies
You can install everything globally (no virtual environment needed):

```bash
python -m pip install --upgrade pip
pip install --user pandas streamlit pyarrow
```

## Step 2 — Run the ETL script

This script:

Reads the raw CSV from data/raw/

Cleans and renames columns (handles Price → UnitPrice, Customer ID → CustomerID)

Computes Revenue = Quantity × UnitPrice

Adds derived columns like Month, Year, OrderDate

Writes a clean dataset to data/processed/sales_clean.csv

Run the ETL:

```bash
python src/etl.py
```


If successful, you’ll see output like:

Reading OnlineRetailII.csv ...
✅ Wrote processed file to: data/processed/sales_clean.csv
Processed rows: 1,000,000+

## Step 3 — Launch the Streamlit Dashboard

Once ETL is done, start the dashboard:

python -m streamlit run app/app.py

Then open the local URL that appears in your terminal (usually http://localhost:8501).

📊 Dashboard Features

Filters:
- Country filter
- Month filter
- Option to include or exclude returns (negative quantities)

KPIs:
- Total Revenue
- Number of Orders
- Average Basket Size
- Unique Customers

Visuals:
- Revenue trend over time (line chart by month)
- Top 15 Products by Revenue
- Top 15 Countries by Revenue
- Download filtered data as CSV

🧠 What this project demonstrates:
- Real-world ETL automation in Python
- Reproducible workflow from raw → clean → dashboard
- End-to-end visualization and analytics
- A clear example of transforming large-scale data into actionable insights

🪄 Next Steps (optional ideas):
- Add a metric showing revenue impact of returns
- Create a “Category” column from product descriptions
- Add a cohort or retention analysis
- Deploy your dashboard publicly using Streamlit Cloud

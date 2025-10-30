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

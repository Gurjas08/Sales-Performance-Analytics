# Sales Performance Analytics

Personal project demonstrating end-to-end analytics: **ETL in Python → cleaned dataset → interactive dashboard**.
Matches resume bullets: automated ETL, large-scale retail data (200K+ rows), and decision-ready visuals.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate     # on Windows: .venv\Scripts\activate
pip install pandas pyarrow streamlit
python src/etl.py
streamlit run app/app.py

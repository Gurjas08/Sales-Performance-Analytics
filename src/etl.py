from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
PROC_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
PROC_DIR.mkdir(parents=True, exist_ok=True)


def load_raw() -> pd.DataFrame:
    files = list(RAW_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSVs found in {RAW_DIR}")
    dfs = []
    for f in files:
        print(f"Reading {f.name} ...")
        dfs.append(pd.read_csv(f, encoding="utf-8"))
    return pd.concat(dfs, ignore_index=True)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    # --- Rename columns to consistent names ---
    rename_map = {
        "Invoice": "Invoice",
        "StockCode": "StockCode",
        "Description": "Description",
        "Quantity": "Quantity",
        "InvoiceDate": "InvoiceDate",
        "Price": "UnitPrice",        # <- changed
        "Customer ID": "CustomerID", # <- changed (removed space)
        "Country": "Country",
    }

    keep = [c for c in rename_map if c in df.columns]
    df = df[keep].rename(columns=rename_map)

    # --- Type cleaning ---
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    df = df.dropna(subset=["InvoiceDate", "Quantity", "UnitPrice"])
    df = df[df["UnitPrice"] > 0]

    # --- Derived metrics ---
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["OrderDate"] = df["InvoiceDate"].dt.date
    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["SalesChannel"] = "Online"

    return df


def write_outputs(df: pd.DataFrame):
    out_csv = PROC_DIR / "sales_clean.csv"
    out_parquet = PROC_DIR / "sales_clean.parquet"

    df.to_csv(out_csv, index=False)
    try:
        df.to_parquet(out_parquet, index=False)
    except Exception as e:
        print(f"Parquet export skipped: {e}")

    print(f"✅ Wrote processed file to: {out_csv}")


def main():
    raw = load_raw()
    clean = transform(raw)
    write_outputs(clean)
    print(f"Processed rows: {len(clean):,}")


if __name__ == "__main__":
    main()

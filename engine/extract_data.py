import pandas as pd
import json

results = {}

# 1. Project Drawdown - GHG impact ranges
try:
    df = pd.read_csv('data/drawdown.csv')
    print("=== DRAWDOWN COLUMNS ===")
    print(df.columns.tolist())
    print("\n=== FIRST 5 ROWS ===")
    print(df.head())
except Exception as e:
    print(f"Drawdown error: {e}")

# 2. Methane emissions
try:
    df2 = pd.read_csv('data/methane.csv')
    print("\n=== METHANE COLUMNS ===")
    print(df2.columns.tolist())
    print("\n=== FIRST 5 ROWS ===")
    print(df2.head())
except Exception as e:
    print(f"Methane error: {e}")

# 3. Electricity mix
try:
    df3 = pd.read_csv('data/electricity.csv')
    print("\n=== ELECTRICITY COLUMNS ===")
    print(df3.columns.tolist())
    print("\n=== FIRST 5 ROWS ===")
    print(df3.head())
except Exception as e:
    print(f"Electricity error: {e}")


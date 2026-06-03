import pandas as pd
import numpy as np

# ── 1. DRAWDOWN ──────────────────────────────────────────────
df = pd.read_csv('data/drawdown.csv')
ghg_col = 'GHG Impact Gt\xa0CO\u2082-eq (100\u2011yr)/yr'

def parse_range(val):
    try:
        parts = str(val).replace('\xa0','').split('to')
        if len(parts) == 2:
            return float(parts[0].strip()), float(parts[1].strip())
        return float(parts[0].strip()), float(parts[0].strip())
    except:
        return None, None

df['low'], df['high'] = zip(*df[ghg_col].apply(parse_range))
df = df.dropna(subset=['low','high'])
df['mid'] = (df['low'] + df['high']) / 2
df['range'] = df['high'] - df['low']

print("=== TOP 10 DRAWDOWN SOLUTIONS BY IMPACT ===")
top = df.nlargest(10, 'mid')[['Solution','low','mid','high','range']]
print(top.to_string())

# ── 2. METHANE ───────────────────────────────────────────────
m = pd.read_csv('data/methane.csv')
world = m[m['Entity'] == 'World'].copy()
recent = world[world['Year'] >= 2000]
fugitive = recent['Fugitive emissions']
agriculture = recent['Agriculture']

print("\n=== METHANE FUGITIVE EMISSIONS (World, 2000-present) ===")
print(f"Mean: {fugitive.mean():.2f}, Std: {fugitive.std():.2f}")
print(f"Min: {fugitive.min():.2f}, Max: {fugitive.max():.2f}")

print("\n=== METHANE AGRICULTURE (World, 2000-present) ===")
print(f"Mean: {agriculture.mean():.2f}, Std: {agriculture.std():.2f}")

# ── 3. ELECTRICITY ───────────────────────────────────────────
e = pd.read_csv('data/electricity.csv')
world_e = e[e['Entity'] == 'World'].copy()
recent_e = world_e[world_e['Year'] >= 2000]

print("\n=== SOLAR SHARE (World, 2000-present) ===")
solar = recent_e['Solar']
print(f"Mean: {solar.mean():.2f}, Std: {solar.std():.2f}")
print(f"Min: {solar.min():.2f}, Max: {solar.max():.2f}")

print("\n=== WIND SHARE (World, 2000-present) ===")
wind = recent_e['Wind']
print(f"Mean: {wind.mean():.2f}, Std: {wind.std():.2f}")


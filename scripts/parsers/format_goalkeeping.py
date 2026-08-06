"""
Parses FBref Goalkeeping table (tab-separated txt).
Save% appears twice (shots + pens) - pandas suffixes the second .1, renamed here.

Usage:
    python3 format_goalkeeping.py
"""
import pandas as pd
from io import StringIO

INPUT_FILE = "data/raw/brazilserieb_gk_raw.csv"
OUTPUT_FILE = "data/clean/brazilserieb_gk_clean.csv"
LEAGUE_NAME = "Brazil Serie B"

RENAME_MAP = {
    "Save%": "Save_pct",
    "Save%.1": "PK_Save_pct",
}

NUMERIC_COLS = [
    "Age", "MP", "Starts", "Min", "90s", "GA", "GA90", "SoTA", "Saves",
    "Save_pct", "W", "D", "L", "CS", "CS%", "PKatt", "PKA", "PKsv", "PKm",
    "PK_Save_pct",
]

with open(INPUT_FILE, encoding="utf-8") as f:
    lines = f.readlines()

header_line_idx = next(i for i, line in enumerate(lines) if line.startswith("Rk\t"))
print(f"Found real header on line {header_line_idx + 1}")

expected_field_count = lines[header_line_idx].rstrip("\n").count("\t") + 1

good_lines = [lines[header_line_idx]]
dropped = 0
for line in lines[header_line_idx + 1:]:
    if not line.strip():
        continue
    field_count = line.rstrip("\n").count("\t") + 1
    if field_count == expected_field_count:
        good_lines.append(line)
    else:
        dropped += 1

if dropped:
    print(f"Warning: dropped {dropped} row(s) with mismatched field counts")

df = pd.read_csv(StringIO("".join(good_lines)), sep="\t")
df = df[df["Rk"] != "Rk"].copy()
df = df.rename(columns=RENAME_MAP)

if "Min" in df.columns:
    df["Min"] = df["Min"].astype(str).str.replace(",", "", regex=False)
    df["Min"] = pd.to_numeric(df["Min"], errors="coerce")

for col in NUMERIC_COLS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

if "Matches" in df.columns:
    df = df.drop(columns=["Matches"])

df["league"] = LEAGUE_NAME

df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} goalkeepers to {OUTPUT_FILE}")
print(df[["Player", "Squad", "MP", "Saves", "Save_pct", "CS", "CS%"]].head(10))
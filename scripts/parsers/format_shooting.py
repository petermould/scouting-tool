"""
Parses FBref player Shooting table (shot volume, accuracy, avg shot distance) - tab-separated txt.

Usage:
    python3 format_shooting.py
"""
import pandas as pd
from io import StringIO

INPUT_FILE = "data/raw/brazilserieb_shooting_raw.csv"
OUTPUT_FILE = "data/clean/brazilserieb_shooting_clean.csv"
LEAGUE_NAME = "Brazil Serie B"

NUMERIC_COLS = ["90s", "Gls", "Sh", "SoT", "SoT%", "Sh/90", "SoT/90",
                "G/Sh", "G/SoT", "PK", "PKatt"]

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

for col in NUMERIC_COLS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

if "Matches" in df.columns:
    df = df.drop(columns=["Matches"])

# keep only join keys + genuinely new shooting-specific columns (Gls already
# exists elsewhere, kept here only to sanity-check the merge later)
keep_cols = ["Player", "Squad", "Sh", "SoT", "SoT%", "Sh/90", "SoT/90", "G/Sh", "G/SoT"]
df = df[[c for c in keep_cols if c in df.columns]]
df["league"] = LEAGUE_NAME

df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} players to {OUTPUT_FILE}")
print(df[["Player", "Squad", "Sh", "SoT%", "Sh/90", "G/Sh"]].head(10))
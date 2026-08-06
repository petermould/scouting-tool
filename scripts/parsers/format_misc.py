"""
Parses FBref Misc Stats table (tab-separated txt).
Stand-in for defensive metrics (tackles won, interceptions, fouls) - FBref has no full Defensive Actions table for these leagues.

Usage:
    python3 format_misc.py
"""
import pandas as pd
from io import StringIO

INPUT_FILE = "data/raw/brazilserieb_misc_raw.csv"
OUTPUT_FILE = "data/clean/brazilserieb_misc_clean.csv"
LEAGUE_NAME = "Brazil Serie B"

NUMERIC_COLS = ["Fls", "Fld", "Off", "Crs", "Int", "TklW", "PKwon", "PKcon", "OG"]

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

keep_cols = ["Player", "Squad"] + [c for c in NUMERIC_COLS if c in df.columns]
df = df[keep_cols]
df["league"] = LEAGUE_NAME

df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} players to {OUTPUT_FILE}")
print(df[["Player", "Squad", "TklW", "Int", "Fls"]].head(10))
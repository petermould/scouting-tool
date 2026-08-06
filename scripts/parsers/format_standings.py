"""
Parses FBref league standings table (final position per team) - tab-separated txt.

Usage:
    python3 format_standings.py
"""
import pandas as pd
from io import StringIO

INPUT_FILE = "data/raw/brazilserieb_standings_raw.csv"
OUTPUT_FILE = "data/clean/brazilserieb_standings_clean.csv"
LEAGUE_NAME = "Brazil Serie B"

with open(INPUT_FILE, encoding="utf-8") as f:
    lines = f.readlines()

# standings tables are headed by "Rk" then "Squad" as the second column
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

# copy/pasting this table often captures "Club Crest " from the team badge
# image's alt-text, stuck in front of the real team name - strip it out
if "Squad" in df.columns:
    df["Squad"] = df["Squad"].astype(str).str.replace("Club Crest ", "", regex=False).str.strip()

df = df.rename(columns={"Rk": "league_position"})
df["league_position"] = pd.to_numeric(df["league_position"], errors="coerce")

# keep just what's needed - final position and team name
keep_cols = ["league_position", "Squad"]
df = df[[c for c in keep_cols if c in df.columns]]

df["league"] = LEAGUE_NAME

df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} teams to {OUTPUT_FILE}")
print(df.to_string(index=False))
"""
Parses FBref "vs Squad" Shooting table (tab-separated txt).
Opponent shots faced - proxy for how much pressure a team was under.

Usage:
    python3 format_shooting_vs.py
"""
import pandas as pd
from io import StringIO

INPUT_FILE = "data/raw/brazilserieb_shooting_vs_raw.csv"
OUTPUT_FILE = "data/clean/brazilserieb_shooting_vs_clean.csv"
LEAGUE_NAME = "Brazil Serie B"

NUMERIC_COLS = ["# Pl", "90s", "Gls", "Sh", "SoT", "SoT%", "Sh/90", "SoT/90",
                "G/Sh", "G/SoT", "PK", "PKatt"]

with open(INPUT_FILE, encoding="utf-8") as f:
    lines = f.readlines()

header_line_idx = next(i for i, line in enumerate(lines) if line.startswith("Squad\t"))
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
df = df[df["Squad"] != "Squad"].copy()

# these rows are labeled "vs Team Name" - strip the "vs " prefix so the
# team name matches everywhere else in the dataset
df["Squad"] = df["Squad"].astype(str).str.replace("^vs ", "", regex=True).str.strip()

for col in NUMERIC_COLS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# rename to make clear these are OPPONENT stats faced, not the team's own
df = df.rename(columns={
    "Sh": "opp_Sh", "SoT": "opp_SoT", "SoT%": "opp_SoT_pct",
    "Sh/90": "opp_Sh_p90", "SoT/90": "opp_SoT_p90",
})

keep_cols = ["Squad", "opp_Sh", "opp_SoT", "opp_SoT_pct", "opp_Sh_p90", "opp_SoT_p90"]
df = df[[c for c in keep_cols if c in df.columns]]
df["league"] = LEAGUE_NAME

df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} teams to {OUTPUT_FILE}")
print(df.to_string(index=False))
"""
Parses FBref Squad Standard Stats table (tab-separated txt), team totals.

Usage:
    python3 format_squads.py
"""
import pandas as pd
from io import StringIO

INPUT_FILE = "data/raw/brazilserieb_squads_raw.csv"
OUTPUT_FILE = "data/clean/brazilserieb_squads_clean.csv"
LEAGUE_NAME = "Brazil Serie B"

RENAME_MAP = {
    "Gls.1": "Gls_p90",
    "Ast.1": "Ast_p90",
    "G+A.1": "G+A_p90",
    "G-PK.1": "G-PK_p90",
    "G+A-PK": "G+A-PK_p90",
}

NUMERIC_COLS = [
    "Age", "MP", "Starts", "90s", "Gls", "Ast", "G+A", "G-PK", "PK", "PKatt",
    "CrdY", "CrdR", "Gls_p90", "Ast_p90", "G+A_p90", "G-PK_p90", "G+A-PK_p90",
]

with open(INPUT_FILE, encoding="utf-8") as f:
    lines = f.readlines()

# squad tables are headed by "Squad" instead of "Rk" (no per-player rank column)
header_line_idx = next(i for i, line in enumerate(lines) if line.startswith("Squad\t"))
print(f"Found real header on line {header_line_idx + 1}, skipping {header_line_idx} line(s) above it")

expected_field_count = lines[header_line_idx].rstrip("\n").count("\t") + 1

good_lines = [lines[header_line_idx]]
dropped = 0
for line in lines[header_line_idx + 1:]:
    if not line.strip():
        continue
    # squad tables sometimes have a trailing "Squad Total"/"Opponent Total" summary row
    if line.startswith("Squad Total") or line.startswith("Opponent Total"):
        continue
    field_count = line.rstrip("\n").count("\t") + 1
    if field_count == expected_field_count:
        good_lines.append(line)
    else:
        dropped += 1

if dropped:
    print(f"Warning: dropped {dropped} row(s) with missing/misaligned fields")

df = pd.read_csv(StringIO("".join(good_lines)), sep="\t")

df = df[df["Squad"] != "Squad"].copy()
df = df.rename(columns=RENAME_MAP)

if "Min" in df.columns:
    df["Min"] = df["Min"].astype(str).str.replace(",", "", regex=False)
    df["Min"] = pd.to_numeric(df["Min"], errors="coerce")

for col in NUMERIC_COLS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

if "Matches" in df.columns:
    df = df.drop(columns=["Matches"])
if "# Pl" in df.columns:
    df = df.rename(columns={"# Pl": "num_players_used"})

df["league"] = LEAGUE_NAME

df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} teams to {OUTPUT_FILE}")
print(df[["Squad", "Gls", "Ast"]].head(30))
"""
Parses FotMob accurate passes/90 leaderboard. 4-line blocks: rank, player, pass success%, passes/90.
Template - reuse for other stat categories, just swap file/column names.

Usage:
    python3 format_fotmob_accpasses.py
"""
import pandas as pd
import re

INPUT_FILE = "data/raw/ligue2_accpasses_fotmob_raw.txt"
OUTPUT_FILE = "data/clean/ligue2_accpasses_clean.csv"
LEAGUE_NAME = "Ligue 2"
SECONDARY_COL_NAME = "PassSuccess_pct"   # what the "Pass success: XX%" line becomes
MAIN_VALUE_COL_NAME = "AccuratePasses_p90"

with open(INPUT_FILE, encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

rows = []
i = 0
while i < len(lines):
    # each block is: rank (number), player name, secondary stat line, main value
    # some FotMob exports have duplicate rank numbers for tied players - just
    # skip past whatever integer sits alone on a line and treat the next line as the name
    if re.fullmatch(r"\d+", lines[i]):
        i += 1
        continue

    player = lines[i]
    secondary_line = lines[i + 1] if i + 1 < len(lines) else ""
    value_line = lines[i + 2] if i + 2 < len(lines) else ""

    secondary_match = re.search(r"[\d.]+", secondary_line)
    secondary_value = float(secondary_match.group()) if secondary_match else None

    value_match = re.search(r"[\d.]+", value_line)
    main_value = float(value_match.group()) if value_match else None

    rows.append({
        "Player": player,
        SECONDARY_COL_NAME: secondary_value,
        MAIN_VALUE_COL_NAME: main_value,
    })
    i += 3

df = pd.DataFrame(rows)
df["league"] = LEAGUE_NAME

df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} players to {OUTPUT_FILE}")
print(df.head(15))
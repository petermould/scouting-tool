"""
Parses FotMob chances created - Brazil Serie B. 4-line blocks: rank, player, chances/90, total.

Usage:
    python3 format_fotmob_chances_brazil.py
"""
import pandas as pd
import re

INPUT_FILE = "data/raw/brazilserieb_chances_fotmob_raw.txt"
OUTPUT_FILE = "data/clean/brazilserieb_chances_clean.csv"
LEAGUE_NAME = "Brazil Serie B"

with open(INPUT_FILE, encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

rows = []
i = 0
while i < len(lines):
    if re.fullmatch(r"\d+", lines[i]):
        i += 1
        continue

    player = lines[i]
    secondary_line = lines[i + 1] if i + 1 < len(lines) else ""
    value_line = lines[i + 2] if i + 2 < len(lines) else ""

    secondary_match = re.search(r":\s*([\d.]+)", secondary_line)
    chances_p90 = float(secondary_match.group(1)) if secondary_match else None

    value_match = re.search(r"[\d.]+", value_line)
    chances_total = float(value_match.group()) if value_match else None

    rows.append({
        "Player": player,
        "ChancesCreated_p90": chances_p90,
        "ChancesCreated_total": chances_total,
    })
    i += 3

df = pd.DataFrame(rows)
df["league"] = LEAGUE_NAME

df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} players to {OUTPUT_FILE}")
print(df.head(15))
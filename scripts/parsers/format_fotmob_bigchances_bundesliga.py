"""
Parses FotMob big chances created - 2. Bundesliga. 4-line blocks: rank, player, assists, big chances.

Usage:
    python3 format_fotmob_bigchances_bundesliga.py
"""
import pandas as pd
import re

INPUT_FILE = "data/raw/bundesliga_bigchances_fotmob_raw.txt"
OUTPUT_FILE = "data/clean/bundesliga_bigchances_clean.csv"
LEAGUE_NAME = "2. Bundesliga"

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
    total_assists = float(secondary_match.group(1)) if secondary_match else None

    value_match = re.search(r"[\d.]+", value_line)
    big_chances = float(value_match.group()) if value_match else None

    rows.append({
        "Player": player,
        "TotalAssists": total_assists,
        "BigChancesCreated": big_chances,
    })
    i += 3

df = pd.DataFrame(rows)
df["league"] = LEAGUE_NAME

df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} players to {OUTPUT_FILE}")
print(df.head(15))
"""
Parses FotMob long balls leaderboard. 4-line blocks: rank, player, success%, long balls/90.

Usage:
    python3 format_fotmob_longballs.py
"""
import pandas as pd
import re

INPUT_FILE = "data/raw/ligue2_longballs_fotmob_raw.txt"
OUTPUT_FILE = "data/clean/ligue2_longballs_clean.csv"
LEAGUE_NAME = "Ligue 2"

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
    long_ball_pct = float(secondary_match.group(1)) if secondary_match else None

    value_match = re.search(r"[\d.]+", value_line)
    long_balls_p90 = float(value_match.group()) if value_match else None

    rows.append({
        "Player": player,
        "LongBallSuccess_pct": long_ball_pct,
        "LongBalls_p90": long_balls_p90,
    })
    i += 3

df = pd.DataFrame(rows)
df["league"] = LEAGUE_NAME

df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} players to {OUTPUT_FILE}")
print(df.head(15))
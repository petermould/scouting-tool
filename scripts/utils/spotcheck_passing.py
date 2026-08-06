"""
Spot-check tool: shows a sample of players with BOTH their original FBref
data (age, position, goals, tackles) and the newly-merged passing data
side by side, so you can visually verify the match makes sense.

Usage:
    python3 spotcheck_passing.py
"""
import pandas as pd

df = pd.read_csv("data/all_players.csv")

display_cols = ["Player", "Squad", "league", "Pos", "Age", "Min",
                 "Gls", "Ast", "TklW",
                 "PassSuccess_pct", "ChancesCreated_p90", "LongBalls_p90"]

# a random sample of 15 players who actually got passing data, across all leagues
has_passing = df["PassSuccess_pct"].notna()
sample = df[has_passing].sample(n=min(15, has_passing.sum()), random_state=42)

print(f"Random sample of {len(sample)} players with merged passing data:\n")
print(sample[display_cols].to_string(index=False))

print("\n\nAny well-known player you want to check specifically? "
      "Edit PLAYER_NAME below and rerun.")

PLAYER_NAME = None  # e.g. "Jack Clarke"
if PLAYER_NAME:
    match = df[df["Player"].str.contains(PLAYER_NAME, case=False, na=False)]
    print(f"\nSearch results for '{PLAYER_NAME}':")
    print(match[display_cols].to_string(index=False))
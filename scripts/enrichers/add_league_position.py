"""
Adds league position + normalised league_success_score (1=top, 0=bottom).

Usage:
    python3 add_league_position.py
"""
import pandas as pd

players = pd.read_csv("data/all_players.csv")
standings = pd.read_csv("data/all_standings.csv")

merged = players.merge(standings, on=["Squad", "league"], how="left")

unmatched = merged[merged["league_position"].isna()][["Squad", "league"]].drop_duplicates()
if len(unmatched):
    print(f"Warning: {len(unmatched)} squad(s) didn't match:")
    print(unmatched.to_string(index=False))

# normalize position to a 0-1 score WITHIN each league (since league sizes
# differ - 24 teams in Championship vs 18 in Bundesliga/Ligue 2), so 1st
# place always scores 1.0 and last place always scores 0.0, regardless of
# how many teams are in that particular league
league_sizes = merged.groupby("league")["league_position"].transform("max")
merged["league_success_score"] = 1 - ((merged["league_position"] - 1) / (league_sizes - 1))
merged["league_success_score"] = merged["league_success_score"].round(3)

merged.to_csv("data/all_players.csv", index=False)
print(f"\nUpdated data/all_players.csv with league position for {len(merged)} players")

print("\nSanity check - one team per league, showing position and score:")
check = merged.drop_duplicates(subset=["Squad", "league"])[
    ["Squad", "league", "league_position", "league_success_score"]
].sort_values(["league", "league_position"])
print(check.groupby("league").first().to_string())
print(check.groupby("league").last().to_string())
"""
Adds team_clean_sheets - summed from each team's keepers' CS totals (only one keeper plays at a time, so this is a clean sum, not double counted).

Usage:
    python3 add_team_clean_sheets.py
"""
import pandas as pd

goalkeepers = pd.read_csv("data/all_goalkeepers.csv")
players = pd.read_csv("data/all_players.csv")

team_clean_sheets = goalkeepers.groupby(["Squad", "league"])["CS"].sum().reset_index()
team_clean_sheets = team_clean_sheets.rename(columns={"CS": "team_clean_sheets"})

print(f"Computed clean sheet totals for {len(team_clean_sheets)} teams")
print(team_clean_sheets.sort_values("team_clean_sheets", ascending=False).head(10).to_string(index=False))

if "team_clean_sheets" in players.columns:
    players = players.drop(columns=["team_clean_sheets"])

merged = players.merge(team_clean_sheets, on=["Squad", "league"], how="left")

unmatched = merged[merged["team_clean_sheets"].isna()][["Squad", "league"]].drop_duplicates()
if len(unmatched):
    print(f"\nWarning: {len(unmatched)} squad(s) didn't match:")
    print(unmatched.to_string(index=False))

merged.to_csv("data/all_players.csv", index=False)
print(f"\nUpdated data/all_players.csv with team_clean_sheets for {len(merged)} players")
"""
Adds % of team goals/assists columns, joined against each team's season totals.

Usage:
    python3 add_team_share.py
"""
import pandas as pd

players = pd.read_csv("data/all_players.csv")
squads = pd.read_csv("data/all_squads.csv")

# keep only the team totals we need, renamed so they don't clash with
# the player's own Gls/Ast columns after merging
team_totals = squads[["Squad", "league", "Gls", "Ast"]].rename(columns={
    "Gls": "team_Gls",
    "Ast": "team_Ast",
})

merged = players.merge(team_totals, on=["Squad", "league"], how="left")

# a couple of leagues have some very minor squad-name spelling differences
# between the player table and squad table (e.g. accents, abbreviations) -
# flag any that failed to match rather than silently producing blank %s
unmatched = merged[merged["team_Gls"].isna()][["Squad", "league"]].drop_duplicates()
if len(unmatched):
    print(f"Warning: {len(unmatched)} squad name(s) didn't match between player and team tables:")
    print(unmatched.to_string(index=False))
    print("(their % columns will be blank - check for spelling differences between the two exports)")

merged["pct_of_team_goals"] = (merged["Gls"] / merged["team_Gls"] * 100).round(1)
merged["pct_of_team_assists"] = (merged["Ast"] / merged["team_Ast"] * 100).round(1)

merged.to_csv("data/all_players.csv", index=False)
print(f"\nUpdated data/all_players.csv with team-share columns for {len(merged)} players")

top_impact = merged.sort_values("pct_of_team_goals", ascending=False)
print("\nTop 10 players by % of team goals scored:")
print(top_impact[["Player", "Squad", "league", "Gls", "team_Gls", "pct_of_team_goals"]].head(10).to_string(index=False))
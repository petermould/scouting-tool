"""
Adds % of team tackles/interceptions. Also re-merges TklW/Int/Fls fresh from all_misc.csv - Brazil's misc data came in after the original merge, needs backfilling.

Usage:
    python3 add_defensive_share.py
"""
import pandas as pd

players = pd.read_csv("data/all_players.csv")
misc = pd.read_csv("data/all_misc.csv")
squad_misc = pd.read_csv("data/all_squad_misc.csv")

# drop any existing misc columns first (from a prior partial merge), then
# re-merge fresh so every league - including newly added ones - gets filled in
misc_cols = ["Fls", "Fld", "Off", "Crs", "Int", "TklW", "PKwon", "PKcon", "OG"]
players = players.drop(columns=[c for c in misc_cols if c in players.columns])
players = players.merge(misc, on=["Player", "Squad", "league"], how="left")

team_totals = squad_misc[["Squad", "league", "TklW", "Int"]].rename(columns={
    "TklW": "team_TklW",
    "Int": "team_Int",
})

merged = players.merge(team_totals, on=["Squad", "league"], how="left")

unmatched = merged[merged["team_TklW"].isna()][["Squad", "league"]].drop_duplicates()
if len(unmatched):
    print(f"Warning: {len(unmatched)} squad(s) didn't match:")
    print(unmatched.to_string(index=False))

merged["pct_of_team_tackles"] = (merged["TklW"] / merged["team_TklW"] * 100).round(1)
merged["pct_of_team_interceptions"] = (merged["Int"] / merged["team_Int"] * 100).round(1)

merged.to_csv("data/all_players.csv", index=False)
print(f"\nUpdated data/all_players.csv with defensive team-share columns for {len(merged)} players")

print("\nTop 10 players by % of team tackles:")
print(merged.sort_values("pct_of_team_tackles", ascending=False)[
    ["Player", "Squad", "league", "Pos", "TklW", "Int", "Fls"]
].head(10).to_string(index=False))
"""
Adds opp shots faced per team + tackles per 100 opp shots faced - so tackles count for more on a team under constant defensive pressure than one rarely threatened.

Usage:
    python3 add_shooting_context.py
"""
import pandas as pd

players = pd.read_csv("data/all_players.csv")
shooting_vs = pd.read_csv("data/all_shooting_vs.csv")

team_context = shooting_vs[["Squad", "league", "opp_Sh", "opp_SoT", "opp_Sh_p90"]].rename(columns={
    "opp_Sh": "team_opp_Sh",
    "opp_SoT": "team_opp_SoT",
    "opp_Sh_p90": "team_opp_Sh_p90",
})

merged = players.merge(team_context, on=["Squad", "league"], how="left")

unmatched = merged[merged["team_opp_Sh"].isna()][["Squad", "league"]].drop_duplicates()
if len(unmatched):
    print(f"Warning: {len(unmatched)} squad(s) didn't match:")
    print(unmatched.to_string(index=False))

# workload-adjusted tackling: tackles made per 100 opponent shots faced -
# rewards defenders on teams under heavy defensive pressure, not just teams
# that happen to tackle a lot in general
merged["tackles_per_100_opp_shots"] = (merged["TklW"] / merged["team_opp_Sh"] * 100).round(2)

merged.to_csv("data/all_players.csv", index=False)
print(f"\nUpdated data/all_players.csv with defensive workload context for {len(merged)} players")

print("\nTop 10 by workload-adjusted tackling (tackles per 100 opponent shots):")
print(merged.sort_values("tackles_per_100_opp_shots", ascending=False)[
    ["Player", "Squad", "league", "Pos", "TklW", "team_opp_Sh", "tackles_per_100_opp_shots"]
].head(10).to_string(index=False))
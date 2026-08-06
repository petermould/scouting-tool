"""
Merges shooting stats (shots, accuracy, shot quality) into all_players.csv, joined on Player+Squad+league - safe here since it's FBref data with real Squad info, unlike the FotMob passing joins.

Usage:
    python3 add_shooting_stats.py
"""
import pandas as pd

players = pd.read_csv("data/all_players.csv")
shooting = pd.read_csv("data/all_shooting.csv")

shooting_cols = ["Sh", "SoT", "SoT%", "Sh/90", "SoT/90", "G/Sh", "G/SoT"]
players = players.drop(columns=[c for c in shooting_cols if c in players.columns], errors="ignore")

merged = players.merge(shooting, on=["Player", "Squad", "league"], how="left")

matched = merged["Sh"].notna().sum()
print(f"Matched shooting data for {matched} out of {len(merged)} players")

merged.to_csv("data/all_players.csv", index=False)
print(f"Updated data/all_players.csv - {len(merged)} total players")

print("\nTop 10 forwards by shots on target %, min 900 minutes:")
forwards = merged[(merged["Pos"].isin(["FW", "FW,MF"])) & (merged["Min"] >= 900) & (merged["Sh"] >= 20)]
print(forwards.sort_values("SoT%", ascending=False)[
    ["Player", "Squad", "league", "Gls", "Sh", "SoT%", "G/Sh"]
].head(10).to_string(index=False))
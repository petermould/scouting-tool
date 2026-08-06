"""
Merges misc stats (tackles, interceptions, fouls, crosses, offsides, penalties) into all_players.csv, joined on Player+Squad+league.

Usage:
    python3 add_misc_stats.py
"""
import pandas as pd

players = pd.read_csv("data/all_players.csv")
misc = pd.read_csv("data/all_misc.csv")

merged = players.merge(misc, on=["Player", "Squad", "league"], how="left")

unmatched = merged[merged["TklW"].isna()][["Player", "Squad", "league"]]
if len(unmatched):
    print(f"Warning: {len(unmatched)} player(s) didn't match to misc stats data:")
    print(unmatched.head(20).to_string(index=False))
    if len(unmatched) > 20:
        print(f"...and {len(unmatched) - 20} more")

merged.to_csv("data/all_players.csv", index=False)
print(f"\nUpdated all_players.csv with defensive/misc columns for {len(merged)} players")

print("\nTop 10 by tackles won:")
print(merged.sort_values("TklW", ascending=False)[
    ["Player", "Squad", "league", "Pos", "TklW", "Int", "Fls"]
].head(10).to_string(index=False))
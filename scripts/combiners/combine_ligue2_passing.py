"""
Combines the 4 separately-scraped FotMob passing stat files for Ligue 2
into one file, merging on Player name.

Usage:
    python3 combine_ligue2_passing.py
"""
import pandas as pd

accpasses = pd.read_csv("data/clean/ligue2_accpasses_clean.csv")[
    ["Player", "PassSuccess_pct", "AccuratePasses_p90"]
]
chances = pd.read_csv("data/clean/ligue2_chances_clean.csv")[
    ["Player", "ChancesCreated_p90", "ChancesCreated_total"]
]
bigchances = pd.read_csv("data/clean/ligue2_bigchances_clean.csv")[
    ["Player", "BigChancesCreated"]
]
longballs = pd.read_csv("data/clean/ligue2_longballs_clean.csv")[
    ["Player", "LongBallSuccess_pct", "LongBalls_p90"]
]

# outer merge - a player might appear in one stat's leaderboard but not
# another (e.g. a low-minutes player might not qualify for every category)
combined = accpasses.merge(chances, on="Player", how="outer")
combined = combined.merge(bigchances, on="Player", how="outer")
combined = combined.merge(longballs, on="Player", how="outer")

combined["league"] = "Ligue 2"

combined.to_csv("data/clean/ligue2_passing_combined.csv", index=False)
print(f"Combined into {len(combined)} unique players")
print(f"Players with data in all 4 stats: {combined.notna().all(axis=1).sum()}")
print(combined.head(10))
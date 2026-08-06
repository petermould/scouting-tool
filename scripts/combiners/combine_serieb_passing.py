"""
Combines the 4 separately-scraped FotMob passing stat files for Serie B
(Italy) into one file, merging on Player name.

Usage:
    python3 combine_serieb_passing.py
"""
import pandas as pd

accpasses = pd.read_csv("data/clean/serieb_accpasses_clean.csv")[
    ["Player", "PassSuccess_pct", "AccuratePasses_p90"]
]
chances = pd.read_csv("data/clean/serieb_chances_clean.csv")[
    ["Player", "ChancesCreated_p90", "ChancesCreated_total"]
]
bigchances = pd.read_csv("data/clean/serieb_bigchances_clean.csv")[
    ["Player", "BigChancesCreated"]
]
longballs = pd.read_csv("data/clean/serieb_longballs_clean.csv")[
    ["Player", "LongBallSuccess_pct", "LongBalls_p90"]
]

combined = accpasses.merge(chances, on="Player", how="outer")
combined = combined.merge(bigchances, on="Player", how="outer")
combined = combined.merge(longballs, on="Player", how="outer")

combined["league"] = "Serie B"

combined.to_csv("data/clean/serieb_passing_combined.csv", index=False)
print(f"Combined into {len(combined)} unique players")
print(f"Players with data in all 4 stats: {combined.notna().all(axis=1).sum()}")
print(combined.head(10))
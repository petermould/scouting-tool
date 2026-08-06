"""
Unifies WhoScored (Championship/Bundesliga) and FotMob (Ligue2/Brazil/SerieB) passing columns into one column per concept - otherwise e.g. KeyPasses_pg is blank for 3 of 5 leagues.

Usage:
    python3 unify_passing_columns.py
"""
import pandas as pd

df = pd.read_csv("data/all_players.csv")

# Creative output: WhoScored calls it "key passes per game", FotMob calls
# it "chances created per 90" - conceptually the same idea (passes leading
# to a shot), close enough to treat as one unified signal
df["creative_output_p90"] = df["KeyPasses_pg"].combine_first(df["ChancesCreated_p90"])

# Long passing range - same idea, different naming convention (per game vs per 90)
df["long_balls_p90"] = df["LongBalls_pg"].combine_first(df["LongBalls_p90"])

# Passing volume - WhoScored gives passes ATTEMPTED, FotMob gives passes
# COMPLETED (accurate) - not identical, but both are a reasonable proxy for
# "how much this player is involved in passing play"
df["passing_volume_p90"] = df["PassesAttempted_pg"].combine_first(df["AccuratePasses_p90"])

# these two are WhoScored-only (no FotMob equivalent) - keep as-is, but
# rename to make clear they're only available for 2 of 5 leagues
df["crosses_p90_partial"] = df["Crosses_pg"]
df["through_balls_p90_partial"] = df["ThroughBalls_pg"]

# PassSuccess_pct is already named identically in both sources - no change needed

df.to_csv("data/all_players.csv", index=False)

print("Added unified columns: creative_output_p90, long_balls_p90, passing_volume_p90")
print("(crosses_p90_partial / through_balls_p90_partial kept as WhoScored-only, marked _partial)")
print()

print("Coverage check - how many players in each league now have creative_output_p90:")
coverage = df.groupby("league")["creative_output_p90"].apply(lambda x: x.notna().sum())
totals = df.groupby("league").size()
for lg in totals.index:
    print(f"  {lg}: {coverage.get(lg, 0)} / {totals[lg]}")
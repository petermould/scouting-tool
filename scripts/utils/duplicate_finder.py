import pandas as pd

df = pd.read_csv("data/all_players.csv")
print("Total rows:", len(df))

dupes = df[df.duplicated(subset=["Player", "Squad", "league"], keep=False)]
print("Rows involved in duplicates:", len(dupes))
print()

if len(dupes) > 0:
    print(dupes[["Player", "Squad", "league", "BigChancesCreated"]].sort_values(["Player", "Squad"]).to_string(index=False))
else:
    print("No duplicates found.")
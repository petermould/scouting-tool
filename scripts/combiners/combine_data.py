import pandas as pd

files = [
    "data/clean/championship_clean.csv",
    "data/clean/bundesliga_clean.csv",
    "data/clean/ligue2_clean.csv",
    "data/clean/serieb_clean.csv",
    "data/clean/brazilserieb_clean.csv",
]

dfs = [pd.read_csv(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)

combined.to_csv("data/all_players.csv", index=False)
print(f"Combined {len(combined)} total players into all_players.csv")
print(combined["league"].value_counts())


import pandas as pd

files = [
    "data/clean/championship_standings_clean.csv",
    "data/clean/bundesliga_standings_clean.csv",
    "data/clean/ligue2_standings_clean.csv",
    "data/clean/serieb_standings_clean.csv",
    "data/clean/brazilserieb_standings_clean.csv",
]

dfs = [pd.read_csv(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)

combined.to_csv("data/all_standings.csv", index=False)
print(f"Combined {len(combined)} total teams into data/all_standings.csv")
print(combined["league"].value_counts())
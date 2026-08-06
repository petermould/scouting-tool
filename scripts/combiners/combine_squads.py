import pandas as pd

files = [
    "data/clean/championship_squads_clean.csv",
    "data/clean/bundesliga_squads_clean.csv",
    "data/clean/ligue2_squads_clean.csv",
    "data/clean/serieb_squads_clean.csv",
    "data/clean/brazilserieb_squads_clean.csv",
]

dfs = [pd.read_csv(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)

combined.to_csv("data/all_squads.csv", index=False)
print(f"Combined {len(combined)} total teams into data/all_squads.csv")
print(combined["league"].value_counts())
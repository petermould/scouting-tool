import pandas as pd

files = [
    "data/clean/championship_shooting_vs_clean.csv",
    "data/clean/bundesliga_shooting_vs_clean.csv",
    "data/clean/ligue2_shooting_vs_clean.csv",
    "data/clean/serieb_shooting_vs_clean.csv",
    "data/clean/brazilserieb_shooting_vs_clean.csv",
]

dfs = [pd.read_csv(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)

combined.to_csv("data/all_shooting_vs.csv", index=False)
print(f"Combined {len(combined)} total teams into data/all_shooting_vs.csv")
print(combined["league"].value_counts())
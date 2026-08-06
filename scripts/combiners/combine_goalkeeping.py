import pandas as pd

files = [
    "data/clean/championship_gk_clean.csv",
    "data/clean/bundesliga_gk_clean.csv",
    "data/clean/ligue2_gk_clean.csv",
    "data/clean/serieb_gk_clean.csv",
    "data/clean/brazilserieb_gk_clean.csv",
]

dfs = [pd.read_csv(x) for x in files]
combined = pd.concat(dfs, ignore_index=True)

combined.to_csv("data/all_goalkeepers.csv", index=False)
print(f"Combined {len(combined)} total goalkeepers into data/all_goalkeepers.csv")
print(combined["league"].value_counts())
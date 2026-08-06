import pandas as pd

files = [
    "data/clean/championship_squad_misc_clean.csv",
    "data/clean/bundesliga_squad_misc_clean.csv",
    "data/clean/ligue2_squad_misc_clean.csv",
    "data/clean/serieb_squad_misc_clean.csv",
    "data/clean/brazilserieb_squad_misc_clean.csv"
]

dfs = [pd.read_csv(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)

combined.to_csv("data/all_squad_misc.csv", index=False)
print(f"Combined {len(combined)} total teams into data/all_squad_misc.csv")
print(combined["league"].value_counts())
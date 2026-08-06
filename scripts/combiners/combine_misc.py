import pandas as pd

files = [
    "data/clean/championship_misc_clean.csv",
    "data/clean/bundesliga_misc_clean.csv",
    "data/clean/ligue2_misc_clean.csv",
    "data/clean/serieb_misc_clean.csv",
    "data/clean/brazilserieb_misc_clean.csv"
]

dfs = [pd.read_csv(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)

combined.to_csv("data/all_misc.csv", index=False)
print(f"Combined {len(combined)} total players into all_misc.csv")
print(combined["league"].value_counts())
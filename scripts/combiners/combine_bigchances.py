import pandas as pd

files = [
    "data/clean/championship_bigchances_clean.csv",
    "data/clean/bundesliga_bigchances_clean.csv",
    "data/clean/ligue2_bigchances_clean.csv",
    "data/clean/serieb_bigchances_clean.csv",
    "data/clean/brazilserieb_bigchances_clean.csv",
]

dfs = [pd.read_csv(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)

combined.to_csv("data/all_bigchances.csv", index=False)
print(f"Combined {len(combined)} total players into data/all_bigchances.csv")
print(combined["league"].value_counts())
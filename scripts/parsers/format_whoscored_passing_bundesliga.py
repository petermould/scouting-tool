"""
Cleans the 2. Bundesliga passing stats pulled via Octoparse from WhoScored.

Usage:
    python3 format_whoscored_passing_bundesliga.py
"""
import pandas as pd
import re

INPUT_FILE = "data/raw/bundesliga_passing_octoparse_raw.csv"
OUTPUT_FILE = "data/clean/bundesliga_passing_clean.csv"
LEAGUE_NAME = "2. Bundesliga"

df = pd.read_csv(INPUT_FILE)

for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].astype(str).str.replace("\t", "", regex=False).str.strip()

df = df.rename(columns={
    "Player": "Rank_num",
    "Player1": "Player",
    "Player3": "Squad",
    "Player4": "Age",
    "Player5": "Pos_raw",
})

df["Squad"] = df["Squad"].str.replace(",", "", regex=False).str.strip()

# WhoScored's German club names differ from FBref's naming convention
SQUAD_NAME_MAP = {
    "Arminia Bielefeld": "Arminia",
    "Darmstadt": "Darmstadt 98",
    "Dynamo Dresden": "Dresden",
    "Eintracht Braunschweig": "BTSV",
    "Fortuna Duesseldorf": "Düsseldorf",
    "Greuther Fuerth": "Greuther Fürth",
    "Hannover": "Hannover 96",
    "Hertha Berlin": "Hertha BSC",
    "Karlsruher SC": "Karlsruher",
    "Nuernberg": "Nürnberg",
    "Paderborn": "Paderborn 07",
    "Preussen Muenster": "Preußen Münster",
    "Schalke": "Schalke 04",
}
df["Squad"] = df["Squad"].replace(SQUAD_NAME_MAP)

print("Unique squad names after mapping (check these match your other data):")
print(sorted(df["Squad"].unique()))

df["Pos_raw"] = df["Pos_raw"].str.replace("^,", "", regex=True).str.strip()

def parse_starts(apps_str):
    match = re.match(r"(\d+)(?:\((\d+)\))?", str(apps_str))
    return int(match.group(1)) if match else None

def parse_sub_apps(apps_str):
    match = re.match(r"\d+\((\d+)\)", str(apps_str))
    return int(match.group(1)) if match else 0

df["Starts"] = df["Apps"].apply(parse_starts)
df["SubApps"] = df["Apps"].apply(parse_sub_apps)

numeric_cols = ["Age", "Mins", "Assists", "KeyP", "AvgP", "PS", "Crosses",
                 "LongB", "ThrB", "Rating"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"-": "0", "": "0", "nan": None})
        df[col] = pd.to_numeric(df[col], errors="coerce")

keep_cols = ["Player", "Squad", "Age", "Pos_raw", "Starts", "SubApps", "Mins",
             "Assists", "KeyP", "AvgP", "PS", "Crosses", "LongB", "ThrB", "Rating"]
df = df[[c for c in keep_cols if c in df.columns]]

df = df.rename(columns={
    "KeyP": "KeyPasses_pg", "AvgP": "PassesAttempted_pg", "PS": "PassSuccess_pct",
    "Crosses": "Crosses_pg", "LongB": "LongBalls_pg", "ThrB": "ThroughBalls_pg",
})

df["league"] = LEAGUE_NAME

df.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved {len(df)} players to {OUTPUT_FILE}")
print(df[["Player", "Squad", "Age", "PassSuccess_pct", "KeyPasses_pg", "ThroughBalls_pg"]].head(15))
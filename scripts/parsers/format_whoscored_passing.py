"""
Cleans WhoScored Championship passing stats pulled via Octoparse.
Octoparse gives confusing column names + stray tab chars - fixes both.

Usage:
    python3 format_whoscored_passing.py
"""
import pandas as pd
import re

INPUT_FILE = "data/raw/championship_passing_octoparse_raw.csv"
OUTPUT_FILE = "data/clean/championship_passing_clean.csv"
LEAGUE_NAME = "Championship"

df = pd.read_csv(INPUT_FILE)

# strip stray tab characters and whitespace from every text/number column
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].astype(str).str.replace("\t", "", regex=False).str.strip()

# rename based on POSITION (Octoparse's auto-generated names don't reflect
# what's actually in each column) rather than trusting the header text
df = df.rename(columns={
    "Player": "Rank_num",  # this is actually just a rank number, not a real column
    "Player1": "Player",
    "Player3": "Squad",
    "Player4": "Age",
    "Player5": "Pos_raw",
})

# clean up Squad - strip trailing ", " first
df["Squad"] = df["Squad"].str.replace(",", "", regex=False).str.strip()

# WhoScored uses shortened team names that don't match FBref's naming
# convention used everywhere else in this project - translate them
SQUAD_NAME_MAP = {
    "Birmingham": "Birmingham City",
    "Charlton": "Charlton Athletic",
    "Coventry": "Coventry City",
    "Derby": "Derby County",
    "Hull": "Hull City",
    "Ipswich": "Ipswich Town",
    "Leicester": "Leicester City",
    "Norwich": "Norwich City",
    "Oxford": "Oxford United",
    "Sheff Wed": "Sheffield Weds",
    "Sheff Utd": "Sheffield United",
    "Stoke": "Stoke City",
    "Swansea": "Swansea City",
    "WBA": "West Brom",
}
df["Squad"] = df["Squad"].replace(SQUAD_NAME_MAP)

print("\nUnique squad names after mapping (check these match your other data):")
print(sorted(df["Squad"].unique()))

# clean up position - strip leading comma and extra whitespace
df["Pos_raw"] = df["Pos_raw"].str.replace("^,", "", regex=True).str.strip()

# Apps sometimes looks like "33(2)" (starts + sub appearances) - split it
def parse_starts(apps_str):
    match = re.match(r"(\d+)(?:\((\d+)\))?", str(apps_str))
    if match:
        return int(match.group(1))
    return None

def parse_sub_apps(apps_str):
    match = re.match(r"\d+\((\d+)\)", str(apps_str))
    if match:
        return int(match.group(1))
    return 0

df["Starts"] = df["Apps"].apply(parse_starts)
df["SubApps"] = df["Apps"].apply(parse_sub_apps)

# numeric columns - WhoScored uses "-" to mean zero for these per-game rates
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
print(f"Saved {len(df)} players to {OUTPUT_FILE}")
print(df[["Player", "Squad", "Age", "PassSuccess_pct", "KeyPasses_pg", "ThroughBalls_pg"]].head(15))
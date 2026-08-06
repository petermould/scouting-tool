"""
Parses FBref Standard Stats (tab-separated txt) for all 4 leagues in one run.

Usage:
    python3 scripts/format_players.py  (run from project root)
"""
import pandas as pd
from io import StringIO

LEAGUES = {
    "Championship": ("data/raw/championship_raw.csv", "data/clean/championship_clean.csv"),
    "2. Bundesliga": ("data/raw/bundesliga_raw.csv", "data/clean/bundesliga_clean.csv"),
    "Ligue 2": ("data/raw/ligue2_raw.csv", "data/clean/ligue2_clean.csv"),
    "Serie B": ("data/raw/serieb_raw.csv", "data/clean/serieb_clean.csv"),
    "Brazil Serie B": ("data/raw/brazilserieb_raw.csv", "data/clean/brazilserieb_clean.csv"),
}

# FBref's "Per 90 Minutes" columns repeat the same names as the "Performance"
# totals columns. pandas auto-suffixes the repeats with ".1" - rename them
# here so both sets are easy to tell apart.
RENAME_MAP = {
    "Gls.1": "Gls_p90",
    "Ast.1": "Ast_p90",
    "G+A.1": "G+A_p90",
    "G-PK.1": "G-PK_p90",
    "G+A-PK": "G+A-PK_p90",
}

NUMERIC_COLS = [
    "Age", "MP", "Starts", "90s", "Gls", "Ast", "G+A", "G-PK", "PK", "PKatt",
    "CrdY", "CrdR", "Gls_p90", "Ast_p90", "G+A_p90", "G-PK_p90", "G+A-PK_p90",
]


def parse_league(input_file, output_file, league_name):
    with open(input_file, encoding="utf-8") as f:
        lines = f.readlines()

    # Auto-detect which line the real header is on (some exports have a blank
    # line + a "Playing Time / Performance / Per 90 Minutes" label line
    # before it, some don't) by finding the first line that starts with "Rk"
    header_line_idx = next(i for i, line in enumerate(lines) if line.startswith("Rk\t"))

    expected_field_count = lines[header_line_idx].rstrip("\n").count("\t") + 1

    # Check every data row has the right number of fields - a row with a
    # missing value doesn't raise an error in pandas, it silently shifts
    # every subsequent column left by one, corrupting the row without warning.
    good_lines = [lines[header_line_idx]]
    dropped = 0
    for line in lines[header_line_idx + 1:]:
        if not line.strip():
            continue
        field_count = line.rstrip("\n").count("\t") + 1
        if field_count == expected_field_count:
            good_lines.append(line)
        else:
            dropped += 1

    df = pd.read_csv(StringIO("".join(good_lines)), sep="\t")
    df = df[df["Rk"] != "Rk"].copy()
    df = df.rename(columns=RENAME_MAP)

    if "Min" in df.columns:
        df["Min"] = df["Min"].astype(str).str.replace(",", "", regex=False)
        df["Min"] = pd.to_numeric(df["Min"], errors="coerce")

    # some leagues (e.g. Brazil Serie B) give Age as "years-days" (e.g. "29-236")
    # instead of a plain integer - take just the years part before converting
    if "Age" in df.columns:
        df["Age"] = df["Age"].astype(str).str.split("-").str[0]
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Matches" in df.columns:
        df = df.drop(columns=["Matches"])

    df["league"] = league_name
    df.to_csv(output_file, index=False)

    print(f"{league_name}: saved {len(df)} players to {output_file}"
          + (f" (dropped {dropped} malformed row(s))" if dropped else ""))
    return df


if __name__ == "__main__":
    for league_name, (input_file, output_file) in LEAGUES.items():
        parse_league(input_file, output_file, league_name)
"""
Merges big chances into all_players.csv, all 5 leagues in one pass - avoids the per-league overwrite bug. Matches on name only (no Squad col in this data) - same accent/nickname normalising as the FotMob passing merges.

Usage:
    python3 add_bigchances.py
"""
import unicodedata
import pandas as pd

CHAR_REPLACEMENTS = {
    "ł": "l", "Ł": "L", "ø": "o", "Ø": "O", "đ": "dj", "Đ": "Dj",
    "æ": "ae", "Æ": "AE", "ß": "ss",
    "þ": "th", "Þ": "Th", "ð": "d", "Ð": "D",
    "ı": "i", "İ": "I",
}

NICKNAME_MAP = {
    "rob atkinson": "robert atkinson", "rob dickie": "robert dickie",
    "matt clarke": "matthew clarke", "sol brynn": "solomon brynn",
    "ben nelson": "benjamin nelson", "alex gilbert": "alexander gilbert",
    "josh griffiths": "joshua griffiths", "mikey johnston": "michael johnston",
    "ali mccann": "alistair mccann", "thomas cannon": "tom cannon",
    "benjamin whiteman": "ben whiteman", "abdul fatawu": "abdul fatawu issahaku",
    "jaden philogene": "jaden philogene bidace", "mattie pollock": "matthew pollock",
    "ben chrisene": "benjamin chrisene", "kayne ramsay": "kayne ramsey",
    "emil riis": "emil riis jakobsen", "joshua key": "josh key",
    "eric-junior bocat": "eric bocat", "bailey cadamarteri": "bailey-tye cadamarteri",
    "kaly sene": "mamadou kaly sene", "mohamed ali zoma": "mohamed zoma",
    "oliver batista meier": "oliver batista-meier", "finn becker": "finn ole becker",
    "luca schuler": "jan luca schuler", "pape diop": "pape demba diop",
    "kim ji-soo": "kim jisoo", "jonas kersken": "jonas thomas kersken",
    "luca itter": "gian-luca itter", "charalambos makridis": "haralambos makridis",
    "marvin marcel schulz": "marvin schulz", "william kokolo": "williams kokolo",
    "kjell watjen": "kjell-arik watjen", "zaid tchibara": "zaid amoussou-tchibara",
    "owono-darnell keumo": "owono keumo", "kenny prince redondo": "kenny redondo",
    "boris mamuzah lum": "boris lum", "juan cabrera": "juan ignacio cabrera",
    "ali eren ersungur": "ali-eren ersungur", "kwon hyeok-kyu": "kwon hyeokkyu",
    "marvin rittmuller": "marvin-lee rittmuller", "grant-leon ranos": "grant ranos",
    "serhat-semih guler": "serhat guler", "john anthony brooks": "john brooks",
}


def normalize_name(name):
    if pd.isna(name):
        return name
    for old, new in CHAR_REPLACEMENTS.items():
        name = name.replace(old, new)
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_name = "".join(c for c in nfkd if not unicodedata.combining(c))
    ascii_name = ascii_name.lower().strip()
    return NICKNAME_MAP.get(ascii_name, ascii_name)


players = pd.read_csv("data/all_players.csv")
bigchances_all = pd.read_csv("data/all_bigchances.csv")

if "BigChancesCreated" in players.columns:
    players = players.drop(columns=["BigChancesCreated", "TotalAssists"], errors="ignore")

players["_join_player"] = players["Player"].apply(normalize_name)

LEAGUES = ["Championship", "2. Bundesliga", "Ligue 2", "Serie B", "Brazil Serie B"]
final_pieces = []

for league_name in LEAGUES:
    bigchances = bigchances_all[bigchances_all["league"] == league_name].copy()
    bigchances["_join_player"] = bigchances["Player"].apply(normalize_name)

    is_this_league = players["league"] == league_name
    league_rows = players[is_this_league].copy()

    name_squad_counts = league_rows.groupby("_join_player")["Squad"].nunique()
    ambiguous_names = name_squad_counts[name_squad_counts > 1].index.tolist()

    bigchances_for_merge = bigchances.drop(columns=["Player", "league"], errors="ignore")
    bigchances_for_merge = bigchances_for_merge[~bigchances_for_merge["_join_player"].isin(ambiguous_names)]

    league_merged = league_rows.merge(bigchances_for_merge, on="_join_player", how="left")

    matched = league_merged["BigChancesCreated"].notna().sum()
    print(f"{league_name}: matched {matched} out of {len(league_rows)} players "
          f"({len(ambiguous_names)} ambiguous name(s) excluded)")

    final_pieces.append(league_merged)

merged = pd.concat(final_pieces, ignore_index=True)
merged = merged.drop(columns=["_join_player"], errors="ignore")

merged.to_csv("data/all_players.csv", index=False)
print(f"\nUpdated data/all_players.csv - {len(merged)} total players")

print("\nFinal coverage check - BigChancesCreated by league:")
coverage = merged.groupby("league")["BigChancesCreated"].apply(lambda x: x.notna().sum())
totals = merged.groupby("league").size()
for lg in totals.index:
    print(f"  {lg}: {coverage.get(lg, 0)} / {totals[lg]}")
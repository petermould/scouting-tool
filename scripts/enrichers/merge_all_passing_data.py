"""
Merges passing for all 5 leagues in one pass - replaces the per-league scripts that kept wiping each other's data. WhoScored (Championship, Bundesliga) matched on Player+Squad; FotMob (Ligue2, Brazil, SerieB) matched on Player only, with small-sample nulling + dupe-name exclusion.

Usage:
    python3 merge_all_passing_data.py
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


def normalize_name(name, use_nicknames=True):
    if pd.isna(name):
        return name
    for old, new in CHAR_REPLACEMENTS.items():
        name = name.replace(old, new)
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_name = "".join(c for c in nfkd if not unicodedata.combining(c))
    ascii_name = ascii_name.lower().strip()
    if use_nicknames:
        return NICKNAME_MAP.get(ascii_name, ascii_name)
    return ascii_name


# ---- Load base dataset and drop any existing passing columns cleanly ----
players = pd.read_csv("data/all_players.csv")

whoscored_cols = ["KeyPasses_pg", "PassesAttempted_pg", "Crosses_pg",
                   "LongBalls_pg", "ThroughBalls_pg", "PassSuccess_pct"]
fotmob_cols = ["PassSuccess_pct", "AccuratePasses_p90", "ChancesCreated_p90",
               "ChancesCreated_total", "BigChancesCreated",
               "LongBallSuccess_pct", "LongBalls_p90"]
all_passing_cols = list(set(whoscored_cols + fotmob_cols))
players = players.drop(columns=[c for c in all_passing_cols if c in players.columns], errors="ignore")

# ---- Part 1: WhoScored data (Championship, 2. Bundesliga) ----
whoscored_passing = pd.concat([
    pd.read_csv("data/clean/championship_passing_clean.csv"),
    pd.read_csv("data/clean/bundesliga_passing_clean.csv"),
], ignore_index=True)[["Player", "Squad"] + whoscored_cols]

players["_join_player"] = players["Player"].apply(normalize_name)
players["_join_squad"] = players["Squad"].apply(normalize_name)
whoscored_passing["_join_player"] = whoscored_passing["Player"].apply(normalize_name)
whoscored_passing["_join_squad"] = whoscored_passing["Squad"].apply(normalize_name)
whoscored_for_merge = whoscored_passing.drop(columns=["Player", "Squad"])

players = players.merge(whoscored_for_merge, on=["_join_player", "_join_squad"], how="left")
ws_matched = players["KeyPasses_pg"].notna().sum()
print(f"WhoScored: matched {ws_matched} players (Championship + 2. Bundesliga)")

# ---- Part 2: FotMob data (Ligue 2, Brazil Serie B, Serie B) - one league at a time ----
FOTMOB_LEAGUES = {
    "Ligue 2": "data/clean/ligue2_passing_combined.csv",
    "Brazil Serie B": "data/clean/brazilserieb_passing_combined.csv",
    "Serie B": "data/clean/serieb_passing_combined.csv",
}

for league_name, filepath in FOTMOB_LEAGUES.items():
    passing = pd.read_csv(filepath)

    # small-sample reliability check
    MIN_IMPLIED_90S = 3
    implied_90s = passing["ChancesCreated_total"] / passing["ChancesCreated_p90"]
    unreliable = implied_90s < MIN_IMPLIED_90S
    rate_cols = ["PassSuccess_pct", "AccuratePasses_p90", "ChancesCreated_p90",
                 "LongBallSuccess_pct", "LongBalls_p90"]
    for col in rate_cols:
        passing.loc[unreliable, col] = pd.NA

    passing["_join_player"] = passing["Player"].apply(normalize_name)

    is_this_league = players["league"] == league_name
    league_rows = players[is_this_league].copy()

    # exclude ambiguous same-named players at different squads within this league
    name_squad_counts = league_rows.groupby("_join_player")["Squad"].nunique()
    ambiguous_names = name_squad_counts[name_squad_counts > 1].index.tolist()

    passing_for_merge = passing.drop(columns=["Player", "league"], errors="ignore")
    passing_for_merge = passing_for_merge[~passing_for_merge["_join_player"].isin(ambiguous_names)]

    league_merged = league_rows.drop(columns=[c for c in fotmob_cols if c in league_rows.columns], errors="ignore")
    league_merged = league_merged.merge(passing_for_merge, on="_join_player", how="left")

    matched = league_merged["PassSuccess_pct"].notna().sum()
    print(f"{league_name}: matched {matched} out of {len(league_rows)} players "
          f"({len(ambiguous_names)} ambiguous name(s) excluded, {unreliable.sum()} small-sample values nulled)")

    # put the merged rows back into the main dataframe
    players = players[~is_this_league]
    players = pd.concat([players, league_merged], ignore_index=True)

players = players.drop(columns=["_join_player", "_join_squad"], errors="ignore")

# ---- Unify into single columns usable regardless of league ----
players["creative_output_p90"] = players["KeyPasses_pg"].combine_first(players["ChancesCreated_p90"])
players["long_balls_p90"] = players["LongBalls_pg"].combine_first(players["LongBalls_p90"])
players["passing_volume_p90"] = players["PassesAttempted_pg"].combine_first(players["AccuratePasses_p90"])
players["crosses_p90_partial"] = players["Crosses_pg"]
players["through_balls_p90_partial"] = players["ThroughBalls_pg"]

players.to_csv("data/all_players.csv", index=False)
print(f"\nUpdated data/all_players.csv - {len(players)} total players")

print("\nFinal coverage check - creative_output_p90 by league:")
coverage = players.groupby("league")["creative_output_p90"].apply(lambda x: x.notna().sum())
totals = players.groupby("league").size()
for lg in totals.index:
    print(f"  {lg}: {coverage.get(lg, 0)} / {totals[lg]}")
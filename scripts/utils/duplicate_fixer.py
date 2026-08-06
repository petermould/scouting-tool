import pandas as pd

df = pd.read_csv("data/all_players.csv")
print("Before dedup:", len(df), "rows")

# use a proper "real identity" key - if Player, Squad, league, Age, and Born
# all match, this is genuinely the same person, regardless of whether some
# incidental column (like Rk, a rank number from the original scrape) differs
identity_cols = ["Player", "Squad", "league", "Age", "Born"]

# show exactly which columns differ within one duplicate group, for transparency
dupes_before = df[df.duplicated(subset=identity_cols, keep=False)]
if len(dupes_before) > 0:
    print(f"\nFound {len(dupes_before)} rows sharing the same identity - checking what differs "
          f"for one example group (Marvin Schulz):")
    example = df[(df["Player"] == "Marvin Schulz") & (df["Squad"] == "Preußen Münster")]
    print(example.to_string())

df_deduped = df.drop_duplicates(subset=identity_cols, keep="first")
print(f"\nAfter dedup on {identity_cols}: {len(df_deduped)} rows")

df_deduped.to_csv("data/all_players.csv", index=False)
print(f"Saved cleaned data/all_players.csv with {len(df_deduped)} players")
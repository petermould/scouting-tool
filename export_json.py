import pandas as pd
import json

forward_ratings = pd.read_csv('data/forward_ratings.csv')
midfielder_ratings = pd.read_csv('data/midfielder_ratings.csv')
tagged_mf_ratings = pd.read_csv('data/tagged_midfielder_ratings.csv')
defender_ratings = pd.read_csv('data/defender_ratings.csv')
goalkeeper_ratings = pd.read_csv('data/goalkeeper_ratings.csv')

def prep(df, subtype_col, subtype_map=None):
    cols = ['Player', 'Squad', 'league', 'rating']
    subtype = df[subtype_col] if subtype_col else 'Goalkeeper'
    out = df[cols].copy()
    out['role'] = subtype
    return out

all_players_web = pd.concat([
    prep(forward_ratings, 'forward_subtype'),
    prep(midfielder_ratings, 'midfielder_subtype'),
    prep(tagged_mf_ratings, 'midfielder_subtype'),
    prep(defender_ratings, 'defender_subtype'),
    goalkeeper_ratings.assign(role='Goalkeeper')[['Player', 'Squad', 'league', 'rating', 'role']],
], ignore_index=True)

all_players_web = all_players_web.sort_values('rating', ascending=False)
all_players_web['rating'] = all_players_web['rating'].round(1)

records = all_players_web.to_dict(orient='records')
with open('players_web.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False)

print(f"Exported {len(records)} players to players_web.json")
print(all_players_web.head(5))
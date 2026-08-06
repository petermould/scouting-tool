import pandas as pd

forward_ratings = pd.read_csv('data/forward_ratings.csv')
defender_ratings = pd.read_csv('data/defender_ratings.csv')

sample_cols = ['Player', 'Squad', 'league', 'Pos', 'Age', 'Gls', 'Ast', 'TklW', 'Int',
               'pct_of_team_goals', 'league_position', 'creative_output_p90', 'rating']

sample = pd.concat([
    forward_ratings[[c for c in sample_cols if c in forward_ratings.columns]],
    defender_ratings[[c for c in sample_cols if c in defender_ratings.columns]],
], ignore_index=True)

sample.sample(30, random_state=1).to_csv('sample_export.csv', index=False)
print("Saved sample_export.csv")
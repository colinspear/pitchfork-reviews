#!/home/cspear/.venv/pitchfork-reviews/bin/python

import pandas as pd
import datetime

# TODO: parameterize for latest artist files
aoty = pd.read_pickle('../data/raw/aoty/2022-04-07_upcoming.pkl')
metacritic_d = pd.read_pickle('../data/raw/metacritic/2022-04-06_coming-soon_date.pkl')
metacritic_nd = pd.read_pickle('../data/raw/metacritic/2022-04-06_coming-soon_no-date.pkl')

a = aoty['name'].str.lower().tolist()
b = metacritic_d['artist_name'].str.lower().tolist()
c = metacritic_nd['artist_name'].str.lower().tolist()

artists = set(a + b + c)

dt = datetime.datetime.today().strftime('%Y-%m-%d')
with open(f"../data/processed/{dt}-artists.txt", 'w') as f:
    f.write('\n'.join(artists))

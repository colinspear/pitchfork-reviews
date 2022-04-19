#!/usr/bin/env python3

from pathlib import Path
import pandas as pd
import datetime as dt

aoty_data = Path("../data/raw/aoty")
metacritic_data = Path("../data/raw/metacritic")

# TODO: parameterize for latest artist files
aoty = pd.read_pickle('../data/raw/aoty/2022-04-07_upcoming.pkl')
metacritic_d = pd.read_pickle('../data/raw/metacritic/2022-04-06_coming-soon_date.pkl')
metacritic_nd = pd.read_pickle('../data/raw/metacritic/2022-04-06_coming-soon_no-date.pkl')

a = aoty['name'].tolist()
b = metacritic_d['artist_name'].tolist()
c = metacritic_nd['artist_name'].tolist()

artists = list(set(a + b + c))

dt = datetime.datetime.today().strftime('%Y-%m-%d')
with open(f"../data/processed/{dt}-artists.txt", 'w') as f:
    f.write('\n'.join(artists))

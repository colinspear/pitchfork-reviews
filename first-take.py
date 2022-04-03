# # The impact of a Pitchfork review on Spotify listeners

# I need:

# - A list of coming album releases
# - Spotify's artist pages, downloaded weekly for each artist putting out a new album
# - Pitchfork reviews, downloaded once a week

import glob
import pickle

from bs4 import BeautifulSoup
import pandas as pd

# AOTY seems more comprehensive that metacritic, but it's easier to parse metacritic so that's what I'm using for now.
# Requests was giving me issues, but curl was easy peasy, so right now dump_metacritic.sh just gets the upcoming releases page and dumps it in a text file in data/raw

# url = "https://www.albumoftheyear.org/upcoming/"
# url = "https://www.metacritic.com/browse/albums/release-date/coming-soon/"


def parse_table(text_html_file):
    with open(text_html_file) as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    c = soup.find_all("table", class_="musicTable")

    album_dict = {}
    album_dict['release_date'] = []
    album_dict['artist_name'] = []
    album_dict['album_title'] = []
    album_dict['comment'] = []
    for i, r in enumerate(c[0].find_all("tr")):
        try:
            _ = r['class']
        except KeyError:
            _ = None
        if _:
            release_date = r.get_text().strip()
        for j, k in enumerate(r.find_all("td")):
            if k['class'][0]=='artistName':
                album_dict['release_date'].append(release_date)
                t = k.get_text().strip()
                if t:
                    album_dict['artist_name'].append(t)
                else:
                    album_dict['artist_name'].append("")
            elif k['class'][0]=='albumTitle':
                t = k.get_text().strip()
                if t:
                    album_dict['album_title'].append(t)
                else:
                    album_dict['album_title'].append("")
            elif k['class'][0]=='dataComment':
                t = k.get_text().strip()
                if t:
                    album_dict['comment'].append(t)
                else:
                    album_dict['comment'].append("")

    return album_dict

raw_files = glob.glob('data/raw/*metacritic-upcoming*.txt')
for rf in raw_files:
    release_table = parse_table(rf)
    with open(f'data/processed/{rf.split("/")[-1].split(".")[0]}.pkl', 'wb') as f:
        pickle.dump(release_table, f)
    
    
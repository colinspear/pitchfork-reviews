#/usr/bin/env sh

curl "https://www.metacritic.com/browse/albums/release-date/coming-soon/date" > "data/raw/$(date +%Y-%m-%d)_metacritic-upcoming-albums.txt"



# # The impact of a Pitchfork review on Spotify listeners

# I need:

# - A list of coming album releases
# - Spotify's artist pages, downloaded weekly for each artist putting out a new album
# - Pitchfork reviews, downloaded once a week

import time
import datetime

from bs4 import BeautifulSoup
import pandas as pd

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# AOTY seems more comprehensive that metacritic, but it's easier to parse metacritic so that's what I'm using for now.
# Requests was giving me issues, but curl was easy peasy, so right now dump_metacritic.sh just gets the upcoming releases page and dumps it in a text file in data/raw

# url = "https://www.albumoftheyear.org/upcoming/"


def get_source(url):
    opts = Options()
    opts.headless=True
    # need to change user-agent to get around bot detection when running headless
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
    with Chrome(options=opts) as driver:
        try:
            driver.get(url)
            # driver.get('https://www.albumoftheyear.org/2022/releases/april-04.php')
            time.sleep(3)
            source = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            # source = driver.find_element(by=By.XPATH, value='//button')
            # source = driver.find_element(by=By.XPATH, value='//largebutton[text()="Show More"]').click()
            return BeautifulSoup(source, 'html.parser')
        except WebDriverException:
            return []


def get_tables(soup):
    return soup.find_all("table", class_="musicTable")


def parse_table(table, has_date=True):
    albums = []
    for r in table.find_all("tr"):
        if r.find("th") and has_date:
            release_date = r.find("th").get_text().strip()
        elif r.find_all("td"):
            cols = r.find_all("td")
            artist_name = cols[0].get_text().strip()
            album_title = cols[1].get_text().strip()
            if has_date:
                comment = cols[2].get_text().strip()
                albums.append((artist_name, album_title, release_date, comment))
            elif not has_date:
                release_date = cols[2].get_text().strip()
                albums.append((artist_name, album_title, release_date))

    return albums


url = "https://www.metacritic.com/browse/albums/release-date/coming-soon/"

print(f"Harvesting Metacritic Coming Soon tables...")
tables = get_tables(get_source(url))

albums_date = pd.DataFrame(
    parse_table(tables[0], has_date=True), 
    columns=['artist_name', 'album_title', 'release_date', 'comment']
)

albums_no_date = pd.DataFrame(
    parse_table(tables[1], has_date=False), 
    columns=['artist_name', 'album_title', 'release_date']
)

print("Harvest complete, dumping harvest in storage silos...")

dt = datetime.datetime.today().strftime('%Y-%m-%d')

ad_string = f"data/raw/metacritic/{dt}_coming-soon_date.pkl"
albums_date.to_pickle(ad_string)
print(f"Data harvest safely written to storage silo {ad_string}")

an_string = f"data/raw/metacritic/{dt}_coming-soon_no-date.pkl"
albums_no_date.to_pickle(an_string)
print(f"Data harvest safely written to storage silo {an_string}")


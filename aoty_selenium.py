# %%
import time
import datetime

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_releases(album_blocks):
    releases = []
    for i, a in enumerate(album_blocks):
        dt = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S%z')
        try:
            release_date = a.find_all('div', {'class': 'date'})[0].get_text()
        except:
            release_date = ""
        try:
            album_title = a.find_all('div', {'class': 'artistTitle'})[0].get_text()
        except:
            album_title = ""
        try:
            artist_name = a.find_all('div', {'class': 'albumTitle'})[0].get_text()
        except:
            artist_name = ""
        releases.append((dt, release_date, album_title, artist_name))
    
    return releases


def get_source(pg_num=''):
    opts = Options()
    opts.headless=True
    # need to change user-agent to get around bot detection when running headless
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
    with Chrome(options=opts) as driver:

        driver.get(f'https://www.albumoftheyear.org/upcoming/{pg_num}')
        # driver.get('https://www.albumoftheyear.org/2022/releases/april-04.php')
        time.sleep(5)
        source = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        # source = driver.find_element(by=By.XPATH, value='//button')
        # source = driver.find_element(by=By.XPATH, value='//largebutton[text()="Show More"]').click()

    soup = BeautifulSoup(source, 'html.parser')
    album_blocks = soup.find_all('div', {'class': 'albumBlock'})
    return get_releases(album_blocks)

# %%
releases = [] 
releases = releases + get_source()

for i in range(1,13):
    releases = releases + get_source(str(i))

# %%
df = pd.DataFrame(releases, columns=['time', 'date', 'title', 'name'])
df
# %%
dt = datetime.datetime.today().strftime('%Y-%m-%d')
df.to_csv("data/raw/aoty/{dt}")
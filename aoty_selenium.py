# %%
import time
import itertools

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


opts = Options()
opts.headless=True
# need to change user-agent to get around bot detection when running headless
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

with Chrome(options=opts) as driver:
    driver.get('https://www.albumoftheyear.org/upcoming')
    time.sleep(5)
    source = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

soup = BeautifulSoup(source, 'html.parser')
album_blocks = soup.find_all('div', {'class': 'albumBlock'})

# %%
releases = {}
releases['release_date'] = []
releases['album_title'] = []
releases['artist_name'] = []

for i, a in enumerate(album_blocks):
    print(i)
    releases['release_date'].append(a.find_all('div', {'class': 'date'})[0].get_text())
    releases['album_title'].append(a.find_all('div', {'class': 'artistTitle'})[0].get_text())
    releases['artist_name'].append(a.find_all('div', {'class': 'albumTitle'})[0].get_text())

print(releases)
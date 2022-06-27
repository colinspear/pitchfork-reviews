#import time
#import datetime
#
#import pandas as pd
#from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
#from selenium.common.exceptions import WebDriverException


opts = Options()
opts.headless=True
# need to change user-agent to get around bot detection when running headless
#opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=opts) 
driver.get(f'https://www.albumoftheyear.org/upcoming/')
 
print(driver.title)
    #time.sleep(5)
    #source = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")


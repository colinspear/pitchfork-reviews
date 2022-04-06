# %%
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.headless=True
# need to change user-agent to get around bot detection when running headless
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

#opts.set_headless()
assert opts.headless  # Operating in headless mode
driver = Chrome(options=opts)
driver.get('https://www.albumoftheyear.org/upcoming')
# time.sleep(8)
driver.title

# %%

driver.quit()
# %%

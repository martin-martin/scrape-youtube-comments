import time
import json
#from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import NoSuchElementException


# --------------------------------------------------------------------
# change chrome path to local installation
chrome_path = "/Users/martin/Documents/codingnomads/nlpython/big_projects/comments/chromedriver"
# change youtube URL to scrape different video's comments
page_url = "https://www.youtube.com/watch?v=AJesAlohO6I&t"  # Chopin!
# --------------------------------------------------------------------

# --------------- PAGE ACCESS ---------------
# accessing the page holding comments (here: youtube)
driver = webdriver.Chrome(executable_path=chrome_path)
driver.get(page_url)
time.sleep(2)  # give the page some time to load

# --------------- FETCH TITLE ---------------
# get the video's title
title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
print(title)

# --------------- LOAD ALL COMMENTS ---------------
# defining the numbers here so we can reference and easily change them
SCROLL_PAUSE_TIME = 2
CYCLES = 7

# we know there's always exactly one HTML element, so let's access it
html = driver.find_element_by_tag_name('html')
# first time needs to not jump to the very end in order to start
html.send_keys(Keys.PAGE_DOWN)  # doing it twice for good measure
html.send_keys(Keys.PAGE_DOWN)  # one time sometimes wasn't enough
# adding extra time for initial comments to load
# if they fail (because too little time allowed), the whole script breaks
time.sleep(SCROLL_PAUSE_TIME * 3)
# and now for loading the hidden comments by scrolling down and up
for i in range(CYCLES):
    html.send_keys(Keys.END)
    time.sleep(SCROLL_PAUSE_TIME)
    # might not be necessary; try out without it.
    # html.send_keys(Keys.PAGE_UP)
    # time.sleep(SCROLL_PAUSE_TIME)



# TODO: combine the below code (which doesn't work on youtube) with the
# solution from above, in order to always scroll to the end of comments
#
# thanks to: https://stackoverflow.com/a/43299513/5717580
#
# # Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")

# while True:
#     # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     print('scrolling...')

#     # Wait to load page
#     time.sleep(SCROLL_PAUSE_TIME)

#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height


# --------------- GETTING THE COMMENT TEXTS ---------------
comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
# pprint(comment_elems)  # for double-checking
all_comments = [elem.text for elem in comment_elems]

# --------------- WRITING TO OUTPUT FILE ---------------
with open('yt_comments.json', 'w') as f:
    json.dump(all_comments, f)


"""
TODO: potential paths forward:
------------------------------
* find title of video to map comments to
* replace title punctuation chars and spaces with underscores for file title
* combine the scrolling approaches to always scroll to the bottom
    without needing to pass an arbitrary magic number
* select instead the complete comment element xpath('//*[@id="body"]')
    - contains text plus additionally author, likes etc.
* add capability to run it for multiple URLs
* transform into a JSON dict that maps file names to comment lists
* append to file instead of overwriting, in order to create a youtube
    comment corpus
"""

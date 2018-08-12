# Scraping Youtube comments with Selenium

This repository holds a basic script to scrape comments from a youtube
video page.

`Selenium` is a convenient way to simulate an end user and thereby get
access to dynamically generated web content that is difficult to scrape
with tools that rely on static pages (e.g. `BeautifulSoup`).

Running the script saves all comment text to a JSON file for further
processing.

---

## TASKS

* find the title of the video (to later map comments to in a JSON structure)
* replace the title's punctuation chars and spaces with underscores (for file title)
* combine both scrolling approaches to always scroll to the bottom
    without needing to pass an arbitrary magic number to the code
* grab the **complete comment element** `xpath('//*[@id="body"]')`
    - contains text plus additionally author, likes etc.
* add capability to run the script for multiple URLs
* transform the output into a JSON dict that maps file names to comment lists
* append to output file instead of overwriting, in order to create a youtube
    comment corpus

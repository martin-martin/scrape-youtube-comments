import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def sm_login(email,password):
    # Browser
    driver = webdriver.Chrome('/Users/martin/Documents/codingnomads/nlpython/big_projects/comments/chromedriver')  # changed to Chromium
    driver.get('https://twitter.com/login')
    # log in
    driver.find_element_by_xpath("//input[@placeholder='Phone, email or username']").send_keys(email)
    driver.find_element_by_xpath("//div[@class='clearfix field']//input[@placeholder='Password']").send_keys(password)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    return driver

# get credentials from open-source-safe environment variables
email = os.environ.get('TWITTER_ACCT')
password = os.environ.get('TWITTER_PWD')


driver = sm_login(email, password)

# post a comment
comment = "<3"

# find the tweet box
tweet_box_path = "//div[@id='tweet-box-home-timeline']"
box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, tweet_box_path)))
box.click()

# insert new tweet comment
driver.execute_script("arguments[0].innerHTML='{}';".format(comment), box)

# click the button
button_path = "//div[@class='home-tweet-box tweet-box component tweet-user']//span[@class='button-text tweeting-text'][contains(text(),'Tweet')]"
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, button_path)))
button.click()

print("tweeted:", comment)

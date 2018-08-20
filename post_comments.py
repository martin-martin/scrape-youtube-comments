# -*- coding: utf-8 -*-

# Python bot for youtube comment
#forked and written by tlh and tdw(original)
import time
import random  # often there's something in the standard library that works!
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def youtube_login(email,password):

    # Browser
    driver = webdriver.Chrome('/Users/martin/Documents/codingnomads/nlpython/big_projects/comments/chromedriver')  # changed to Chromium
    driver.get('https://accounts.google.com/ServiceLogin?hl=en&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26feature%3Dsign_in_button%26app%3Ddesktop%26action_handle_signin%3Dtrue%26next%3D%252F&uilel=3&passive=true&service=youtube#identifier')

    # log in
    # //*[@id="identifierId"]
    driver.find_element_by_id("identifierId").send_keys(email)
    driver.find_element_by_id('identifierNext').click()
    # //*[@id="password"]/div[1]/div/div[1]/input
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
    driver.find_element_by_id('passwordNext').click()

    return driver

def comment_page(driver,urls,comment):

    # Check if there still urls
    if len( urls ) == 0:
        print('Youtube Comment Bot: Finished!')
        return []

    # Pop a URL from the array
    url = urls.pop()

    # Visite the page
    driver.get(url)
    driver.implicitly_wait(1)

    # Is video avaliable (deleted,private) ?
    if not check_exists_by_xpath(driver,'//*[@id="movie_player"]'):
        print("can't find movie player")
        return comment_page(driver, urls, random_comment())

    # Scroll, wait for load comment box
    driver.execute_script("window.scrollTo(0, 500);")

    # Comments are disabled?
    if check_exists_by_xpath(driver,'//*[@id="comments-disabled-message"]/div/span'):
        print("comments are disabled")
        return comment_page(driver, urls, random_comment())

    # Lets wait for comment box
    print("scrolled. waiting for comments to load...")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "commentbox")))  # changed this

    # Activate box for comments
    driver.find_element_by_xpath("//div[@id='creation-box']").click()

    # Send comment and post
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//*[@id="comment-simplebox"]/div[1]').send_keys(comment)
    driver.find_element_by_xpath('//*[@id="comment-simplebox"]/div[1]').send_keys(Keys.ENTER + Keys.ENTER)

    # Is post ready to be clicked?
    post = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="comment-simplebox"]/div[3]/button[2]'))
    )
    post.click()

    # Lets wait a bit
    r = random.randint(2,5)
    time.sleep(r)

    # Recursive
    return comment_page(driver, urls, random_comment())


def random_comment():

    messages = [
        'Whats up?',
        'Nice video!',
        'Yoyoyo'
    ]

    r = random.choice(messages)  # changed this, more clear even with standards
    return r

def check_exists_by_xpath(driver,xpath):

    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        print('Could not find the element!')
        return False

    return True

if __name__ == '__main__':

    # Credentials
    email = 'XXXXXX'
    password = 'XXXXXX'


    # List of Urls
    urls = [
      'https://www.youtube.com/watch?v=Awf45u6zrP0',
      'https://www.youtube.com/watch?v=kkFFq11j6dQ'
    ]

    # You can add in a file and import from there
    '''
    inp = open ("urls.txt","r")
    for line in inp.readlines():
            urls.append(line.split())
      '''
    # Login in youtube

    driver = youtube_login(email, password)

    # Random comment
    comment_page(driver,urls,random_comment())

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
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.PAGE_DOWN)  # doing it twice for good measure
    time.sleep(2)
    html.send_keys(Keys.PAGE_DOWN)  # one time sometimes wasn't enough
    time.sleep(2)
    html.send_keys(Keys.PAGE_UP)

    # Comments are disabled?
    if check_exists_by_xpath(driver,'//*[@id="message"]'):
        print("comments are disabled")
        return comment_page(driver, urls, random_comment())

    # Lets wait for comment box
    print("scrolled. waiting for comments to load...")
    commentbox_path = "/html[1]/body[1]/ytd-app[1]/div[1]/ytd-page-manager[1]/ytd-watch-flexy[1]/div[3]/div[1]/div[1]/ytd-comments[1]"
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, commentbox_path)))  # changed this
    print("found comment box!")

    # --------- TRYING WITH TABS -----------
    # sort_by_path = "/html[1]/body[1]/ytd-app[1]/div[1]/ytd-page-manager[1]/ytd-watch-flexy[1]/div[3]/div[1]/div[1]/div[7]/div[3]/ytd-video-secondary-info-renderer[1]/div[1]/ytd-expander[1]/div[1]/div[1]/yt-formatted-string[1]/a[19]"
    # sort_by_elem = driver.find_element_by_xpath(sort_by_path)
    # print("found SORT elem: ", sort_by_elem)
    # sort_by_elem.click()
    # print("clicked...")
    # print("trying to TAB and ENTER")
    # sort_by_elem.send_keys(Keys.SHIFT + Keys.TAB)
    # print("success?!")
    # sort_by_elem.send_keys(Keys.ENTER)


    # --------- TRYING WITH CLICKS ----------
    # Activate box for comments
    simple_box_path = "/html[1]/body[1]/ytd-app[1]/div[1]/ytd-page-manager[1]/ytd-watch-flexy[1]/div[3]/div[1]/div[1]/ytd-comments[1]/ytd-item-section-renderer[1]/div[1]/ytd-comments-header-renderer[1]/div[5]"
    outer_box = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, simple_box_path)))
    print("located outer comment box")
    outer_box.click()
    print("clicked outer box")
    # sort_by_elem = driver.find_element_by_xpath(sort_by_path)
    # comment_box_path = "/html[1]/body[1]/ytd-app[1]/div[1]/ytd-page-manager[1]/ytd-watch-flexy[1]/div[3]/div[1]/div[1]/ytd-comments[1]/ytd-item-section-renderer[1]/div[1]/ytd-comments-header-renderer[1]/div[5]/ytd-comment-simplebox-renderer[1]/div[1]"
    # comment_elem = driver.find_element_by_xpath(comment_box_path)
    # comment_elem.click()
    # print("clicked on comment box")

    # here youtube redirects me to yet another signin page, thereby breaking
    # the script. let's try to try-except forward from here

    try:
        # Send comment and post
        textarea_path = "/html[1]/body[1]/ytd-app[1]/div[1]/ytd-page-manager[1]/ytd-watch-flexy[1]/div[3]/div[1]/div[1]/ytd-comments[1]/ytd-item-section-renderer[1]/div[1]/ytd-comments-header-renderer[1]/div[5]/ytd-comment-simplebox-renderer[1]/div[3]/ytd-comment-dialog-renderer[1]/ytd-commentbox[1]/div[1]/div[1]/paper-input-container[1]/div[1]/div[1]/iron-autogrow-textarea[1]/div[2]/textarea[1]"
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, textarea_path)))  # changed this
        driver.implicitly_wait(5)
        text_elem = driver.find_element_by_xpath(textarea_path)
        text_elem.click()
        text_elem.send_keys(comment)
        text_elem.send_keys(Keys.ENTER)

        # Is post ready to be clicked?
        button_path = "/html[1]/body[1]/ytd-app[1]/div[1]/ytd-page-manager[1]/ytd-watch-flexy[1]/div[3]/div[1]/div[1]/ytd-comments[1]/ytd-item-section-renderer[1]/div[1]/ytd-comments-header-renderer[1]/div[5]/ytd-comment-simplebox-renderer[1]/div[3]/ytd-comment-dialog-renderer[1]/ytd-commentbox[1]/div[1]/div[2]/div[4]/ytd-button-renderer[2]/a[1]/paper-button[1]"
        post = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, button_path))
        )
        post.click()

        # Lets wait a bit
        r = random.randint(2,5)
        time.sleep(r)

        # Recursive
        return comment_page(driver, urls, random_comment())

    except:
        # log in
        # //*[@id="identifierId"]
        driver.find_element_by_id("identifierId").send_keys(email)
        driver.find_element_by_id('identifierNext').click()
        # //*[@id="password"]/div[1]/div/div[1]/input
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
        driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
        driver.find_element_by_id('passwordNext').click()

        # after renewed login, try again
        return comment_page(driver, urls, random_comment())



def random_comment():

    messages = [
        'Whats up?',
        '<3',
        'Yolo'
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
    email = os.environ.get('GOOGLE_ACCT')
    password = os.environ.get('GOOGLE_PWD')


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

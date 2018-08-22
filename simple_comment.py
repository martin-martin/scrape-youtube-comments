import os
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
    driver.find_element_by_id("identifierId").send_keys(email)
    driver.find_element_by_id('identifierNext').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
    driver.find_element_by_id('passwordNext').click()
    return driver

email = os.environ.get('GOOGLE_ACCT')
password = os.environ.get('GOOGLE_PWD')
print(email, password)
driver = youtube_login(email, password)

# post a comment
comment = "test"

box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "box")))
box.click()

frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="+1"]')))
driver.switch_to.frame(frame)

driver.find_element_by_xpath('//div[@onclick]').click()

element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@jsname="msEQQc"]/following-sibling::div//div[@g_editable="true"]')))
driver.execute_script("arguments[0].innerHTML='%s';" % comment, element)

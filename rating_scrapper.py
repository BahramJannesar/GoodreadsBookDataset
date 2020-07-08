from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from goodreads import client
import os
import requests
import time
import re
from bs4 import BeautifulSoup
import json


user_id = 1
chromedriver = "driver/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
actions = ActionChains(driver)
username_login = 'ba.jannesar@gmail.com'
password_login = 'elnazghazalnilofar'



login_link = 'https://www.goodreads.com/user/sign_in'
driver.get(login_link)


username_input = driver.find_element_by_xpath('//*[(@id = "user_email")]')
password_input = driver.find_element_by_xpath('//*[(@id = "user_password")]')

username_input.send_keys(username_login)
password_input.send_keys(password_login)

login_button = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gr-button--large", " " ))]')
login_button.click()


driver.get('https://www.goodreads.com/review/list/4622890-emily-may?per_page=100&shelf=read')


book_titles = driver.find_elements_by_css_selector('#booksBody .title a')
book_rating = driver.find_elements_by_css_selector('.rating .value')
person_rating = {
    
        'ID' : 4622890 ,
    }
for title , rating in zip(book_titles, book_rating):

    person_rating.update({title.text : rating.text})



person_rating_js = json.dumps(person_rating, indent=4 ,ensure_ascii=False)
with open('person_rating.json', 'a') as file:
    file.write(person_rating_js + ',')




































# if __name__ == "__main__":

#     login(driver , username_login ,password_login)



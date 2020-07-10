from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from goodreads import client
import os
import requests
import time
import re
from bs4 import BeautifulSoup
import json
import math



chromedriver = "driver/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
chrome_option = Options()
chrome_option.add_argument("--headless")
chrome_option.add_argument("--disable-gpu")
chrome_option.add_argument("--no-sandbox")
chrome_option.add_argument("--window-size=1920,1200")
chrome_option.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(chromedriver , chrome_options=chrome_option)
actions = ActionChains(driver)

user_id = 1
username_login = ''
password_login = ''


def login(driver , username_login ,password_login):

    login_link = 'https://www.goodreads.com/user/sign_in'
    driver.get(login_link)
    time.sleep(5)

    username_input = driver.find_element_by_xpath('//*[(@id = "user_email")]')
    password_input = driver.find_element_by_xpath('//*[(@id = "user_password")]')

    username_input.send_keys(username_login)
    password_input.send_keys(password_login)

    login_button = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gr-button--large", " " ))]')
    login_button.click()



def rating_scraper(user_id , driver):

    while user_id < 1000 :
        try:        
            driver.get('https://www.goodreads.com/review/list/{}?per_page=100&shelf=read'.format(user_id))

            time.sleep(3)
            counts_of_rating = int(driver.find_element_by_css_selector('#header .greyText').text[1:-1])
            count_of_rating_page = math.ceil(counts_of_rating / 100)


            person_rating = {

                        'ID' : user_id ,
                    }

            if counts_of_rating == 0 :

                person_rating['Rating'] = 'This user doesn\'t have any rating'

            elif counts_of_rating >= 1 and counts_of_rating <= 100 :

                for page_number in range(count_of_rating_page):
                    time.sleep(3)
                    book_titles = driver.find_elements_by_css_selector('#booksBody .title a')
                    book_rating = driver.find_elements_by_css_selector('.rating .value')

                    for title , rating in zip(book_titles, book_rating):
                        if rating.text is not "":
                            person_rating[title.text] = rating.text
                
            else :
                for page_number in range(count_of_rating_page):
                    time.sleep(3)
                    book_titles = driver.find_elements_by_css_selector('#booksBody .title a')
                    book_rating = driver.find_elements_by_css_selector('.rating .value')

                    for title , rating in zip(book_titles, book_rating):
                        if rating.text is not "":
                            person_rating[title.text] = rating.text

                    timeout = 10
                    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[(@id = "reviewPagination")]//*[contains(concat( " ", @class, " " ), concat( " ", "next_page", " " ))]')))
                    button_next_page = driver.find_element_by_css_selector('#reviewPagination .next_page')
                    button_next_page.click()



            person_rating_js = json.dumps(person_rating, indent=4 ,ensure_ascii=False)
            with open('person_rating.json', 'a') as file:
                print('User id number {} Done!'.format(user_id))
                file.write(person_rating_js + ',')


            user_id += 1
        except:
            print('User id number {} doesn\'t exist!'.format(user_id))
            user_id += 1



if __name__ == "__main__":

    login(driver , username_login ,password_login)

    rating_scraper(user_id , driver)


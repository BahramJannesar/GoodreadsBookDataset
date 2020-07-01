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

limit_of_page_review = 0
book_id = 1
chromedriver = "driver/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
actions = ActionChains(driver)
username_login = 'ba.jannesar@gmail.com'
password_login = 'elnazghazalnilofar'


def login(driver , username_login ,password_login):
    login_link = 'https://www.goodreads.com/user/sign_in'
    driver.get(login_link)


    username_input = driver.find_element_by_xpath('//*[(@id = "user_email")]')
    password_input = driver.find_element_by_xpath('//*[(@id = "user_password")]')

    username_input.send_keys(username_login)
    password_input.send_keys(password_login)

    login_button = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gr-button--large", " " ))]')
    login_button.click()




def review_scraper_generator(book_id , driver):

    while book_id < 1000000 :
        
        book_link = 'https://www.goodreads.com/book/show/{}'.format(book_id)

        print(book_link)

        driver.get(book_link)
        timeout = 10
        try:
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "next_page", " " ))]')))
        except: 
            pass
        book_name = driver.find_element_by_xpath('//*[(@id = "bookTitle")]')

        counts_of_text_review = str(driver.find_element_by_css_selector(
            '.gr-hyperlink~ .gr-hyperlink').text)
        counts_of_text_review = re.sub(
            r'(\s[a-z]*)', '', counts_of_text_review, flags=re.MULTILINE)
        counts_of_text_review = int(
            re.sub(r'(\,)', '', counts_of_text_review, flags=re.MULTILINE))

        print(type(counts_of_text_review))

        if (counts_of_text_review / 30) >= 10:
            limit_of_page_review = 10
        elif (counts_of_text_review / 30) < 10 and (counts_of_text_review / 30) > 1:
            limit_of_page_review = counts_of_text_review / 30
        elif (counts_of_text_review / 30) <= 1 and (counts_of_text_review / 30) > 0:
            limit_of_page_review = 1


        i = -2
        reviwe_list = []
        if counts_of_text_review != 0:
            while i < limit_of_page_review:

                source_page = driver.page_source
                soup = BeautifulSoup(source_page, 'html.parser')
                reviews = soup.find_all('span', attrs={'class': 'readable'})

                for review in reviews:
                    review = re.sub(r'\.*(more)', '', review.text)
                    review = re.sub(
                        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', review)

                    reviwe_list.append(review)

                if limit_of_page_review > 1:
                    time.sleep(4)
                    button_next_page = driver.find_element_by_xpath(
                        '//*[contains(concat( " ", @class, " " ), concat( " ", "next_page", " " ))]')
                    button_next_page.click()
                    i += 1
                else:
                    break

            book_dic = {
                            "Id": int(book_id),
                            "BookName": book_name.text,
                            "reviews": reviwe_list

            }


            yield book_dic

        else:
            book_dic = {
                        "Id": int(book_id),
                        "BookName": book_name.text,
                        "reviews": 'This book dosent have any text review'

                    }

            yield book_dic

        book_id += 1


if __name__ == "__main__":

    login(driver , username_login ,password_login)

    for book , book_id in review_scraper_generator(book_id , driver):
        print('Reviews of the book number {} , Done!'.format(book_id))
        book_js = json.dumps(book, indent=4)
        with open('books_reviews.json', 'a') as file:
            file.write(book_js + ',')
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
chromedriver = "driver/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
actions = ActionChains(driver)


base_url = 'https://www.goodreads.com/book/show/'

book_id = input('Book ID : ')


project_link = base_url + book_id
print(project_link)

driver.get(project_link)

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
elif (counts_of_text_review / 30) <= 1 and (counts_of_text_review / 30) > 0 :
    limit_of_page_review = 1


print(limit_of_page_review)

i = 1
reviwe_list = []
if counts_of_text_review != 0:
    while i <= limit_of_page_review:

        reviews = driver.find_elements_by_xpath(
            '//*[(@id = "bookReviews")]//*[contains(concat( " ", @class, " " ), concat( " ", "readable", " " ))]//span')

        for each in reviews:
            print(each.text)
            reviwe_list.append(each.text)
        time.sleep(4)
        button_next_page = driver.find_element_by_xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "next_page", " " ))]')
        button_next_page.click()
        i = 1 + i

    book_dic = {
                    "Id": int(book_id),
                    "BookName": book_name,
                    "reviews": reviwe_list

                }

    book_js = json.dumps(book_dic, indent=4)
    with open('book.json', 'w') as file:
        file.write(book_js)
else:
    book_dic = {
                "Id": int(book_id),
                "BookName": book_name.text,
                "reviews": 'This book dosent have any text review'

            }
    book_js = json.dumps(book_dic, indent=4)
    with open('book.json', 'w') as file:
        file.write(book_js)

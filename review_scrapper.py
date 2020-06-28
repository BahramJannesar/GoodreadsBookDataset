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
elif (counts_of_text_review / 30) <= 1 and (counts_of_text_review / 30) > 0:
    limit_of_page_review = 1


print(limit_of_page_review)

i = 0
reviwe_list = []
if counts_of_text_review != 0:
    while i < limit_of_page_review:

        # spolier_reviews = driver.find_elements_by_css_selector('em a')
        # for spoiler_button in spolier_reviews:
        #     spoiler_button.click()

        # read_more_button = driver.find('#bookReviews .readable:nth-child(1) > a')
        # for read_button in read_more_button:
        #     read_button.click()

        likes_number = driver.find_elements_by_xpath(
            '//*[(@id = "bookReviews")]//*[contains(concat( " ", @class, " " ), concat( " ", "likesCount", " " ))]')
        source_page = driver.page_source
        soup = BeautifulSoup(source_page, 'html.parser')
        reviews = soup.find_all('div', attrs={'class': 'reviewText stacked'})

        for review, like in zip(reviews, likes_number):
            review = re.sub(r'\.*(more)', '', review.text)
            review = re.sub(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', review)
            first_part_of_review = review[0:500]
            second_part_of_review = review[500:-1]

            if len(first_part_of_review) > len(second_part_of_review):
                with open('book.txt', 'a') as file:
                    file.write(first_part_of_review + '\n')
            else:
                with open('book.txt', 'a') as file:
                    file.write(second_part_of_review + '\n')

        if limit_of_page_review > 1:
            time.sleep(4)
            button_next_page=driver.find_element_by_xpath(
                '//*[contains(concat( " ", @class, " " ), concat( " ", "next_page", " " ))]')
            button_next_page.click()
            i=1 + i
        else:
            break

#     book_dic = {
#                     "Id": int(book_id),
#                     "BookName": book_name.text,
#                     "reviews": reviwe_list[62:-1]

#     }

#     book_js = json.dumps(book_dic, indent=4)
#     with open('book.json', 'w') as file:
#         file.write(book_js)
# else:
#     book_dic = {
#                 "Id": int(book_id),
#                 "BookName": book_name.text,
#                 "reviews": 'This book dosent have any text review'

#             }
#     book_js = json.dumps(book_dic, indent=4)
#     with open('book.json', 'w') as file:
#         file.write(book_js)

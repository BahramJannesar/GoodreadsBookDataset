from goodreads import client
import json
import time
import requests


api_key = 'PpYBUoitliItUuI1DJpw'
api_token = 'UvfyWFTlE9PIlG1Mrmd025333p5wKDcEwD1R1Skiw'
book_list = []
all_book_title = []
book_number = 76757


gc = client.GoodreadsClient(api_key, api_token)


def API_json(gc, book_number, all_book_title, book_list):
    while(book_number < 76760):
        try:
            book = gc.book(book_number)
            dist = book.rating_dist
            #seprator = ';'
            #KharCode = str(book.title) + seprator + str(book.authors[0]) + seprator + str(book.isbn) + seprator + str(book.language_code) + seprator + str(book.publication_date) + seprator + str(book.publisher) + seprator + str(book.num_pages) + seprator + str(book.rating_dist) + seprator + str(book.average_rating) + seprator + str(book.format) + seprator + str(book.is_ebook) + seprator + str(book.text_reviews_count) + seprator + str(book.gid) + "\n"
            book_dic = {
                "Id": str(book_number),
                "Name": str(book.title),
                "Authors": str(book.authors[0]),
                "ISBN": book.isbn,
                "Rating": float(book.average_rating),
                "PublishYear": int(book.publication_date[2]),
                "PublishMonth": int(book.publication_date[1]),
                "PublishDay": int(book.publication_date[0]),
                "Publisher": book.publisher,
                "RatingDist5": dist.split('|')[0],
                "RatingDist4": dist.split('|')[1],
                "RatingDist3": dist.split('|')[2],
                "RatingDist2": dist.split('|')[3],
                "RatingDist1": dist.split('|')[4],
                "RatingDistTotal": dist.split('|')[5],
                "CountsOfReview": int(book.text_reviews_count),
                "Language": book.language_code,
                "pagesNumber": int(book.num_pages),
            }
            if book.title not in all_book_title:
                book_list.append(book_dic)
                yield book_dic

            all_book_title.append(book.title)
            can_str = 'Book number {} read.'.format(book_number)
            print(can_str)
            book_number += 1
            time.sleep(1)

        except:
            cant_str = 'Cant read {} book information.'.format(book_number)
            print(cant_str)
            book_number += 1
            time.sleep(1)


for each in API_json(gc, book_number, all_book_title, book_list):
    book_js = json.dumps(each, indent=4)
    with open('book.json', 'a') as file:
        file.write(book_js + ',')

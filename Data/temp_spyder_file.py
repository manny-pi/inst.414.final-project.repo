# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import requests
import json

kaggle_data = pd.read_csv("books.csv")  # read the Kaggle books dataset
isbn_13 = kaggle_data['isbn13']         # extract the ISBN-13 column

isbn_13.shape 

test = isbn_13.head(5)

# create an empty list to store the book data
book_data_list = []
url_base = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'

# iterate over the ISBN 13 numbers, and get the information we need using the Google Books API
for i, isbn in enumerate(test):

    # generate the URL for the Google Books API search 
    url = url_base + isbn

    # get the book data; convert it to a dictionary using .json()
    book_data = requests.get(url).json()

    print(f'{i} {isbn}: {book_data.keys()}', end=': ')
    
    if 'totalItems' in book_data and book_data['totalItems'] > 0:

        print(book_data['totalItems'], end=': ')
        print(book_data['items'][0]['volumeInfo']['title'], end='')
        # extract the relevant fields and create a new row in the DataFrame
        book = {
            'title': book_data['items'][0]['volumeInfo'].get('title', ''),
            'subtitle': book_data['items'][0]['volumeInfo'].get('subtitle', ''),
            'authors': book_data['items'][0]['volumeInfo'].get('authors', ''),
            'publisher': book_data['items'][0]['volumeInfo'].get('publisher', ''),
            'publishdate': book_data['items'][0]['volumeInfo'].get('publishedDate', ''),
            'description': book_data['items'][0]['volumeInfo'].get('description', ''),
            'isbn_13': isbn,
            'page_count': book_data['items'][0]['volumeInfo'].get('pageCount', ''),
            'main_categories': book_data['items'][0]['volumeInfo'].get('categories', ''),
            'categories': book_data['items'][0]['volumeInfo'].get('categories', ''),
            'average_rating': book_data['items'][0]['volumeInfo'].get('averageRating', ''),
            'ratings_count': book_data['items'][0]['volumeInfo'].get('ratingsCount', ''),
            'maturity_rating': book_data['items'][0]['volumeInfo'].get('maturityRating', '')
        }

        # append the new dictionary to the book_data_list
        book_data_list.append(book)
    else:

        # handle the case where no results were returned for the ISBN-13 number
        # print(f"No results found for ISBN-13 {isbn}")
        pass
    
    print()

# convert the list of dictionaries to a DataFrame
response_df = pd.DataFrame(book_data_list)

test_book = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:9780439655484').json()


import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
import requests
import datetime
import logging
import pandas as pd


logger = setup_logger('db_helper')


@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="25682397",
        database="book_buddy"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

###BOOK BUDDY FUNCTIONS
def insert_genre(name):
    logger.info(f"insert_genre called: {name}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO genres (name) VALUES (%s)", (name,)
        )

def insert_author(name):
    logger.info(f"insert_author called: {name}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO authors (name) VALUES (%s)", (name,)
        )

def insert_book(title, author_id, genre_id, total_pages, rating):
    logger.info(f"insert_book called: {title}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO books (title, author_id, genre_id, total_pages, rating) VALUES (%s,%s,%s,%s,%s)", (title, author_id, genre_id, total_pages, rating)
        )

def insert_progress(book_id,pages_read,progress_date):
    logger.info(f"insert_progress called for: {book_id}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO reading_progress(book_id,pages_read,progress_date) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE pages_read = VALUES(pages_read), progress_date = VALUES(progress_date)", (book_id,pages_read,progress_date)
        )


def fetch_books():
    logger.info(f"fetching all books")
    with get_db_cursor() as cursor:
        cursor.execute('''SELECT a.title, a.total_pages, b.name as author, c.name as genre, concat(round(d.pages_read/a.total_pages,2)*100,'%') as progress
                FROM books as a
                LEFT JOIN authors as b
	            ON a.author_id = b.author_id
                LEFT JOIN genres as c
	            ON a.genre_id = c.genre_id
	            LEFT JOIN reading_progress as d
	            ON a.book_id = d.book_id;''')
        books = cursor.fetchall()
        return books

###END BOOK BUDDY FUNCTIONS

def fetch_recommendations(title=None, author=None):
    """
    Fetch recommended books from Google Books API based on a title and optional author.
    """

    GOOGLE_BOOKS_API_KEY = "AIzaSyBbpAAWlJ0nI572GAb5Mjjbm08G0GZuOPE"  # Replace with your API Key

    query = f"intitle:{title}"
    if author:
        query += f"+inauthor:{author}"

    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"

    response = requests.get(url)
    if response.status_code == 200:
        books = response.json().get("items", [])
        recommendations = [
            {
                "title": book["volumeInfo"].get("title", "Unknown Title"),
                "author": ", ".join(book["volumeInfo"].get("authors", ["Unknown Author"])),
                "description": book["volumeInfo"].get("description", "No description available."),
                "link": book["volumeInfo"].get("infoLink", "#"),
            }
            for book in books[:5]  # Limit to top 5 recommendations
        ]
        return recommendations
    else:
        print(f"Error: {response.status_code}, {response.text}")  # Handle API errors
        return []

# # Google Books API URL
# query = "python programming"
# api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
#
# # Send request
# response = requests.get(api_url)
#
# # Check response
# if response.status_code == 200:
#     data = response.json()
#     print(data.get('items', []))  # List of books
# else:
#     print(f"Error: {response.status_code}, {response.text}")


if __name__ == "__main__":

    #new_author = insert_author("Anthony Bordain")
    #new_genre = insert_genre("Biography")
    #new_book = insert_book("Atomic Habits",2,2,306,4.6)
    #my_library = fetch_books()
    #df = pd.DataFrame(my_library)
    #print(df)
    recommendations1 = fetch_recommendations(title='India')
    print(recommendations1)

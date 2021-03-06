import sqlite3
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


# ---------------------- INITIATE AND POPULATE DB ------------------------- #
CREATE_BOOKS_TABLE = """CREATE TABLE IF NOT EXISTS books (bookid INTEGER PRIMARY KEY, 
              title TEXT, author TEXT, genre TEXT, FOREIGN KEY(genre) references genres(book_genre))"""
INSERT_BOOK = "INSERT INTO books VALUES (NULL, ?, ?, ?)"


CREATE_MEMBERS_TABLE = "CREATE TABLE IF NOT EXISTS members (memberid INTEGER PRIMARY KEY, member_name TEXT, email TEXT)"
INSERT_MEMBER = "INSERT INTO members VALUES (NULL, ?, ?)"


CREATE_RATING_TABLE = """CREATE TABLE IF NOT EXISTS ratings (book_id INTEGER, member_id INTEGER, rating REAL, 
                FOREIGN KEY (book_id) REFERENCES books(bookid), 
                FOREIGN KEY (member_id) REFERENCES members(memberid))"""
INSERT_RATING = """INSERT INTO ratings (book_id, member_id, rating) 
               VALUES ((SELECT bookid FROM books WHERE books.title=(?)),
              (SELECT memberid FROM members WHERE members.email=(?)), ?)"""


CREATE_GENRE_TABLE = "CREATE TABLE IF NOT EXISTS genres (genreid INTEGER PRIMARY KEY, book_genre TEXT)"
INSERT_GENRE = "INSERT INTO genres VALUES (NULL, ?)"


# ----------------------------------- QUERIES -------------------------------- #
VIEW_BOOKS = """SELECT books.bookid, books.title, books.author, books.genre, ROUND(AVG(ratings.rating),1) as book_rating 
              FROM books LEFT JOIN ratings ON ratings.book_id = books.bookid
              GROUP BY books.bookid ORDER BY book_rating DESC"""
VIEW_MEMBERS = "SELECT * FROM members"
VIEW_GENRES = "SELECT genre, COUNT(*) FROM books GROUP BY genre"

SEARCH_BOOK = """SELECT books.bookid, books.title, books.author, books.genre, ROUND(AVG(ratings.rating), 1) as book_rating
              FROM books LEFT JOIN ratings ON books.bookid = ratings.book_id 
              WHERE title=(?)"""
SEARCH_MEMBER = """SELECT members.member_name, members.email, COUNT(ratings.rating) 
                FROM members LEFT JOIN ratings ON members.memberid=ratings.member_id
                WHERE member_name=(?)"""
SEARCH_GENRE = """SELECT books.title, books.author, genres.book_genre FROM books
                LEFT JOIN genres ON books.genre=genres.book_genre
                WHERE genre=(?)"""
SEARCH_BY_RATING = """SELECT books.bookid, books.title, books.author, books.genre, ratings.rating FROM books
                    LEFT JOIN ratings ON books.bookid=ratings.book_id
                    WHERE ratings.rating=(?)"""

# ------------------------------------- DELETE/UPDATE ----------------------------- #
DELETE_BOOK = "DELETE FROM books WHERE title=?"
DELETE_MEMBER = "DELETE FROM members WHERE email=?"
DELETE_RATING = """CREATE TRIGGER delete_rating AFTER DELETE ON books BEGIN
                DELETE FROM ratings WHERE book_id=(?) END"""

UPDATE_BOOK = "UPDATE books SET title=?, author=?, genre=? WHERE bookid=(?)"
UPDATE_MEMBER = "UPDATE members SET member_name=?, email=? WHERE memberid=(?)"
UPDATE_GENRE = """CREATE TRIGGER update_genre AFTER UPDATE ON books
                BEGIN UPDATE genres SET book_genre=? END"""


# ---------------------- INITIATE AND POPULATE DB ------------------------- #
def connect():
    return sqlite3.connect("bookclub.db")


def create_tables(connection):
    with connection:
        connection.execute(CREATE_BOOKS_TABLE)
        connection.execute(CREATE_GENRE_TABLE)
        connection.execute(CREATE_MEMBERS_TABLE)
        connection.execute(CREATE_RATING_TABLE)


def add_book(connection, title, author, genre):
    with connection:
        connection.execute(INSERT_BOOK, (title, author, genre))


def add_member(connection, member_name, email):
    with connection:
        connection.execute(INSERT_MEMBER, (member_name, email))


def add_genre(connection, book_genre):
    with connection:
        connection.execute(INSERT_GENRE, (book_genre,))


def add_rating(connection, title, member_email, rating):
    with connection:
        connection.execute(INSERT_RATING, (title, member_email, rating))

# ----------------------------------- QUERIES -------------------------------- #


def view_books(connection):
    with connection:
        # For displaying rows as a list of tuples change the pd.read_sql_query command to the following:

        # rows = connection.execute(VIEW_BOOKS).fetchall()
        # for row in rows:
        #     print(row)

        print(pd.read_sql_query(VIEW_BOOKS, connection, index_col=['bookid']))


def view_members(connection):
    with connection:
        # rows = connection.execute(VIEW_MEMBERS).fetchall()
        # for row in rows:
        #     print(row)
        print(pd.read_sql_query(VIEW_MEMBERS, connection, index_col=['memberid']))


def view_genres(connection):
    with connection:
        rows = connection.execute(VIEW_GENRES).fetchall()
        for row in rows:
            print(row)


def search_book(connection, title):
    with connection:
        rows = connection.execute(SEARCH_BOOK, (title,)).fetchall()
        for row in rows:
            print(row)


def search_member(connection, member_name):
    with connection:
        rows = connection.execute(SEARCH_MEMBER, (member_name,)).fetchall()
        for row in rows:
            print(row)


def search_genre(connection, genre):
    with connection:
        rows = connection.execute(SEARCH_GENRE, (genre,)).fetchall()
        for row in rows:
            print(row)


def search_by_ratings(connection, rating):
    with connection:
        rows = connection.execute(SEARCH_BY_RATING, (rating,)).fetchall()
        for row in rows:
            print(row)


# ------------------------------------- DELETE/UPDATE ------------------------------- #

def delete_book(connection, title):
    with connection:
        connection.execute(DELETE_BOOK, (title,))


def delete_member(connection, email):
    with connection:
        connection.execute(DELETE_MEMBER, (email,))


def delete_rating(connection, book_id):
    with connection:
        connection.execute(DELETE_RATING, (book_id,))


def update_book(connection, title, author, genre, bookid):
    with connection:
        connection.execute(UPDATE_BOOK, (title, author, genre, bookid))


def update_member(connection, member_name, email, memberid):
    with connection:
        connection.execute(UPDATE_MEMBER, (member_name, email, memberid))


def update_genre(connection, book_genre):
    with connection:
        connection.execute(UPDATE_GENRE, (book_genre,))




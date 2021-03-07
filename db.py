import sqlite3


# ---------------------- INITIATE/POPULATE ------------------------- #
CREATE_BOOKS_TABLE = """CREATE TABLE IF NOT EXISTS books (bookid INTEGER PRIMARY KEY, 
              title TEXT, author TEXT, genre TEXT)"""
INSERT_BOOK = "INSERT INTO books VALUES (NULL, ?, ?, ?)"


CREATE_MEMBERS_TABLE = "CREATE TABLE IF NOT EXISTS members (memberid INTEGER PRIMARY KEY, member_name TEXT, email TEXT)"
INSERT_MEMBER = "INSERT INTO members VALUES (NULL, ?, ?)"


CREATE_RATING_TABLE = """CREATE TABLE IF NOT EXISTS ratings (ratingid INTEGER PRIMARY KEY, book_id INTEGER, member_id INTEGER, rating REAL, 
                FOREIGN KEY (book_id) REFERENCES books(bookid), 
                FOREIGN KEY (member_id) REFERENCES members(memberid))"""
INSERT_RATING = """INSERT INTO ratings (book_id, member_id, rating) 
               VALUES ((SELECT bookid FROM books WHERE books.title=(?)),
              (SELECT memberid FROM members WHERE members.email=(?)), ?)"""


# ----------------------------------- FETCH/SEARCH -------------------------------- #
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
SEARCH_GENRE = """SELECT books.bookid, books.title, books.author, books.genre, ROUND(AVG(ratings.rating), 1) as book_rating
                FROM books LEFT JOIN ratings ON books.bookid = ratings.book_id  
                WHERE genre=(?) GROUP BY books.bookid"""

# ------------------------------------- DELETE/UPDATE ----------------------------- #
DELETE_BOOK = "DELETE FROM books WHERE title=?"
DELETE_MEMBER = "DELETE FROM members WHERE email=?"
DELETE_RATING = """CREATE TRIGGER delete_rating AFTER DELETE ON books BEGIN
                DELETE FROM ratings WHERE ratings.book_id=books.bookid END"""

UPDATE_BOOK = "UPDATE books SET title=?, author=?, genre=? WHERE bookid=(?)"
UPDATE_MEMBER = "UPDATE members SET member_name=?, email=? WHERE memberid=(?)"


# ---------------------- INITIATE/POPULATE ------------------------- #
def connect():
    return sqlite3.connect("bookclub.db")


def create_tables(connection):
    with connection:
        connection.execute(CREATE_BOOKS_TABLE)
        connection.execute(CREATE_MEMBERS_TABLE)
        connection.execute(CREATE_RATING_TABLE)


def add_book(connection, title, author, genre):
    with connection:
        connection.execute(INSERT_BOOK, (title, author, genre))


def add_member(connection, member_name, email):
    with connection:
        connection.execute(INSERT_MEMBER, (member_name, email))


def add_rating(connection, title, member_email, rating):
    with connection:
        connection.execute(INSERT_RATING, (title, member_email, rating))

# ----------------------------------- FETCH/SEARCH -------------------------------- #


def view_books(connection):
    with connection:
        rows = connection.execute(VIEW_BOOKS).fetchall()
        for row in rows:
            print(row)


def view_members(connection):
    with connection:
        rows = connection.execute(VIEW_MEMBERS).fetchall()
        for row in rows:
            print(row)


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


# --------------------------- SEND EMAIL ------------------------- #
def send_email(connection):
    with connection:
        rows = connection.execute(VIEW_MEMBERS).fetchall()
        member_list = []
        for row in rows:
            member_list.append(row[2])
        print(member_list)




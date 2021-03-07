import sqlite3
import db


APP_MENU = """
 ___________________
|   BOOKCLUB APP    |
| __________________|
 ________________________________________________
|Please choose one of these options (type 1-14): |
|       * BOOKS *                                |        
|1 - Add a new book.                             |
|2 - View all the books (sorted by rating).      |
|3 - Find a book (by title).                     |
|4 - Find books (by genre).                      |
|5 - View all genres.                            |
|6 - Delete a book (by title).                   |
|7 - Update book (by bookid).                    |
|        * MEMBERS *                             |
|8 - Add a new member.                           |
|9 - View all members.                           |
|10 - Find member and number of books read.      |
|11 - Delete a member (by email).                |
|12 - Update member.                             |
|        ***                                     |
|13 - Add book rating from a member (by email).  |
|        ***                                     |
|14 - EXIT                                       | 
|________________________________________________|
Your selection: 
"""


def menu():
    connection = db.connect()
    db.create_tables(connection)

    while True:
        user_input = input(APP_MENU)
        if user_input == "1":
            menu_add_book_data(connection)
        elif user_input == "2":
            menu_view_books(connection)
        elif user_input == "3":
            menu_search_book(connection)
        elif user_input == "4":
            menu_search_genre(connection)
        elif user_input == "5":
            menu_view_genres(connection)
        elif user_input == "6":
            menu_delete_book(connection)
        elif user_input == "7":
            menu_update_book(connection)
        elif user_input == "8":
            menu_add_member_data(connection)
        elif user_input == "9":
            menu_view_members(connection)
        elif user_input == "10":
            menu_find_member(connection)
        elif user_input == "11":
            menu_delete_member(connection)
        elif user_input == "12":
            menu_update_member(connection)
        elif user_input == "13":
            menu_add_rating(connection)
        elif user_input == "14":
            print("Exiting the program.")
            break

        else:
            print("Invalid input. Please try again!")


# ---------------------------- FUNCTIONS FOR THE MENU ----------------------- #

# Send email to all members
def send_email_to_members(connection):
    pass


# 1 - Add a new book.
def menu_add_book_data(connection):
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    genre = input("Enter book genre: ")
    db.add_book(connection, title, author, genre)
    print("{} added to the database.".format(title))


# 2 - View all the books (sorted by rating).
def menu_view_books(connection):
    print("BookID, Title, Author, Genre, Rating:\n")
    db.view_books(connection)


# 3 - Find a book by title.
def menu_search_book(connection):
    title = input("Enter book title: ")
    print("BookID, Title, Author, Genre, Rating:\n")
    db.search_book(connection, title)


# 4 - Find a book by genre.
def menu_search_genre(connection):
    genre = input("Enter genre: ")
    print("BookID, Title, Author, Genre, Rating:\n")
    db.search_genre(connection, genre)


# 5 - View all genres.
def menu_view_genres(connection):
    db.view_genres(connection)


# 6 - Delete a book by title.
def menu_delete_book(connection):
    title_to_delete = input("Enter title to delete: ")
    db.delete_book(connection, title_to_delete)
    print("Book {} deleted".format(title_to_delete))


# 7 - Update book by bookid.
def menu_update_book(connection):
    new_title = input("New title: ")
    new_author = input("New author: ")
    new_genre = input("New genre: ")
    bookid = input("Enter ID of the book you want to update: ")
    db.update_book(connection, new_title, new_author, new_genre, bookid)
    print("Book updated.")


# 8 - Add a new member.
def menu_add_member_data(connection):
    member_name = input("Enter member name: ")
    member_email = input("Enter member email: ")
    db.add_member(connection, member_name, member_email)
    print("{} added to the list.".format(member_name))


# 9 - View all members.
def menu_view_members(connection):
    db.view_members(connection)


# 10 - Find member by name.
def menu_find_member(connection):
    name = input("Enter member name to search for: ")
    db.search_member(connection, name)


# 11 - Delete a member by email.
def menu_delete_member(connection):
    email = input("Enter email of a member you want to remove: ")
    db.delete_member(connection, email)
    print("Member removed.")


# 12 - Update member.
def menu_update_member(connection):
    member_name = input("Enter new name: ")
    member_email = input("Enter new email: ")
    memberid = input("Enter ID of the member you want to edit: ")
    db.update_member(connection, member_name, member_email, memberid)
    print("Member updated.")


# 13 - Add book rating from a member (by email).
def menu_add_rating(connection):
    book_title = input("Enter book title: ")
    email = input("Enter member email: ")
    rating = float(input("Enter book rating (1-10): "))

    db.add_rating(connection, book_title, email, rating)
    print("Rating {} added for {} by {}".format(rating, book_title, email))


menu()

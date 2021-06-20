from app import db
from app.models import Book, Author, Category
from flask_restful import abort

class Book(Book):

    def __init__(self, book_id):
        if self.__check_existance(int(book_id)):
            self.__decompose(self.raw)
            print('Book obj. created')
        else:
            abort(404, message="Book with id={} does not exist".format(book_id))

    def get_book_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'published_date': self.published_date,
            'authors': self.authors_list,
            'categories': self.categories,
            'average_rating': self.average_rating,
            'ratings_count': self.ratings_count,
            'thumbnail': self.thumbnail
        }

    def __decompose(self, book):
        self.id = book.book_id
        self.title = book.title
        self.published_date = self.__get_date_str(book)
        self.authors_list = self.__get_names(book.authors)
        self.categories_list = self.__get_names(book.categories)
        self.average_rating = book.average_rating
        self.ratings_count = book.ratings_count
        self.thumbnail = book.thumbnail

    def __check_existance(self, book_id):
        try:
            self.raw = self.query.get(int(book_id))

            return True
        except:
            return False

    def __get_names(self, iterable_obj):
        buffer = []

        for obj in iterable_obj:
            buffer.append(obj.name)

        return buffer

    def __get_date_str(self, book):
        return str(book.published_day) + "." + str(book.published_month) + "." + str(book.published_year)

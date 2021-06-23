from app import db
from app.models import Book, Author, Category
from flask_restful import abort
from copy import deepcopy

class Books_manager(Book):
    #load book from the database
    def load_book(self, book_id):
        if self.__check_existence(book_id):
            self.__decompose(self.raw)
        else:
            abort(404, message="Book with id={} does not exist".format(book_id))


    #raw dataset processor
    def add_dataset(self, dataset):
        for book in dataset:
            if not self.__check_existence(book['book_id']):
                book_id = book['book_id'] if book['book_id'] else None
                title = book['title'] if book['title'] else None
                date = self.__date_processor(book['published_date'])
                published_day = date[2]
                published_month = date[1]
                published_year = date[0]
                average_rating = int(book['average_rating']) if book['average_rating'] else None
                ratings_count = int(book['ratings_count']) if book['ratings_count'] else None
                thumbnail = book['thumbnail'] if book['thumbnail'] else None
                authors = book['authors'] if book['authors'] else []
                categories = book['categories'] if book['categories'] else []

                new_book = Book(book_id=book_id, title=title, published_day=published_day, published_month=published_month,
                              published_year=published_year, average_rating=average_rating, ratings_count = ratings_count,
                              thumbnail = thumbnail)

                self.__add_book(new_book)
                self.__commit_dataset()
                self.__asign_with_authors(book_id, authors)
                self.__asign_with_categories(book_id, categories)

            else:
                db.session.commit()


    #returns finished book json
    def get_book_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'published_date': self.published_date,
            'authors': self.authors_list,
            'categories': self.categories_list,
            'average_rating': self.average_rating,
            'ratings_count': self.ratings_count,
            'thumbnail': self.thumbnail
        }


    #returns books sorted by year if order is given or just books by year if year is given
    def get_books_by_year(self, order=None, year=None):
        ids = []

        if year:
            books = Book.query.filter_by(published_year=year).all()
            if not books:
                abort(404, message="Books with year={} does not exist".format(year))
        else:
            books = Book.query.order_by(Book.published_year).all()

        for book in books:
            ids.append(book.book_id)

        if order == "-":
            ids.reverse()

        return self.get_all_books(ids)

    #gets all book_ids from the database
    def __get_all_ids(self):
        book_ids = []

        books = Book.query.all()

        for book in books:
            book_ids.append(book.book_id)

        return book_ids

    #returns all books from the certain id range
    #returns all books by default
    def get_all_books(self, ids=None):
        quantity = 0
        book_ids=ids

        if not book_ids:
            book_ids = self.__get_all_ids()

        books = []

        for book_id in book_ids:
            quantity +=1

            self.load_book(book_id=book_id)
            books.append(self.get_book_dict())

        return {
            "quantity": quantity,
            "books": books
        }


    #returns prepared date data for the database
    def __date_processor(self, published_date):
        date = published_date.split("-")

        if len(date) == 3:
            return [date[0], date[1], date[2]]
        elif len(date) == 2:
            return [date[0], date[1], None]
        elif len(date) == 1:
            return [date[0], None, None]


    #assigns book with its author
    def __asign_with_authors(self, book_id, authors):
        book = self.__get_book_by_id(book_id)

        for author in authors:
            book.authors.append(author)

        db.session.commit()


    #assigns book with its category
    def __asign_with_categories(self, book_id, categories):
        book = self.__get_book_by_id(book_id)

        for category in categories:
            book.categories.append(category)

        db.session.commit()

    #decomposes book for get_book_dict dunction
    def __decompose(self, book):
        self.id = book.book_id
        self.title = book.title
        self.published_date = self.__get_date_str(book)
        self.authors_list = self.__get_names(book.authors)
        self.categories_list = self.__get_names(book.categories)
        self.average_rating = book.average_rating
        self.ratings_count = book.ratings_count
        self.thumbnail = book.thumbnail

    #checks if book exist. also saves the book for the optimization
    def __check_existence(self, book_id):
        self.raw = self.__get_book_by_id(book_id)

        if self.raw:
            return True

        return False

    #returns name property of the certain object
    def __get_names(self, iterable_obj):
        buffer = []

        for obj in iterable_obj:
            buffer.append(obj.name)

        return buffer


    #returns prepared date string
    def __get_date_str(self, book):
        date = ""

        if not book.published_day and not book.published_month and book.published_year:
            date = str(book.published_year)
        elif not book.published_day and  book.published_month and book.published_year:
            date = str(book.published_year) + "-" + str(book.published_month)
        else:
            date = str(book.published_year) + "-" + str(book.published_month) + "-" + str(book.published_day)

        return date


    #adds book into the session
    def __add_book(self, new_book_obj):
        db.session.add(new_book_obj)


    #get book by its book_id
    def __get_book_by_id(self, book_id):
        return Book.query.filter_by(book_id=book_id).first()


    #commits
    def __commit_dataset(self):
        db.session.commit()
        db.session.remove()
        db.session.close()


class Authors_manager(Author):

    #inserts authors objects into the dataset
    def add_authorship(self, dataset):
        dataset_processed = dataset
        books_counter = 0
        authors_counter = 0

        for book in dataset_processed:
            book['authors'] = book['authors'] if book['authors'] else []
            for author in book['authors']:
                if self.__check_existence(author):
                    author_obj = deepcopy(self.raw)
                    dataset_processed[books_counter]['authors'][authors_counter] = author_obj
                else:
                    author_obj = Author(name = author)

                    db.session.add(author_obj)
                    self.__commit()
                    self.__check_existence(author)
                    author_obj = deepcopy(self.raw)
                    dataset_processed[books_counter]['authors'][authors_counter] = author_obj


                authors_counter += 1

            books_counter += 1
            authors_counter = 0

        return dataset_processed


    #returns books ids assigned with the certain author
    def get_authors_books_ids(self, name):
        author = Author.query.filter_by(name=name).first()

        if not author:
            return None

        ids = []

        for book in author.books.all():
            ids.append(book.book_id)

        return ids


    #returns a deep copy of the author objects.
    #here's a bug with dinamic relations that I dont know how to fix :'(
    def get_author(self, name):
        self.__check_existence(name)

        return deepcopy(self)


    #check the authors existence
    def __check_existence(self, name):
        self.raw = Author.query.filter_by(name=name).first()

        if self.raw:
            return True

        return False


    #commits
    def __commit(self):
        db.session.commit()
        db.session.remove()
        db.session.close()


#the same thing as the Author manager but with categories
#I made another class for the obvious usage
class Categories_manager(Category):

    def add_category_affiliation(self, dataset):
        dataset_processed = dataset
        books_counter = 0
        categories_counter = 0

        for book in dataset_processed:
            book['categories'] = book['categories'] if book['categories'] else []
            for category in book['categories']:
                if self.__check_existence(category):
                    category_obj = deepcopy(self.raw)
                    dataset_processed[books_counter]['categories'][categories_counter] = category_obj
                else:
                    category_obj = Category(name = category)

                    db.session.add(category_obj)
                    self.__commit()
                    self.__check_existence(category)
                    category_obj = deepcopy(self.raw)
                    dataset_processed[books_counter]['categories'][categories_counter] = category_obj


                categories_counter += 1

            books_counter += 1
            categories_counter = 0

        return dataset_processed

    def __check_existence(self, name):
        self.raw = Category.query.filter_by(name=name).first()

        if self.raw:
            return True

        return False

    def __commit(self):
        db.session.commit()
        db.session.remove()
        db.session.close()



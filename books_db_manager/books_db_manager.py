from app import db
from app.models import Book, Author, Category
from flask_restful import abort
from copy import deepcopy

class Books_manager(Book):

    def load_book(self, book_id):
        if self.__check_existance(book_id):
            self.__decompose(self.raw)
        else:
            abort(404, message="Book with id={} does not exist".format(book_id))

    def add_dataset(self, dataset):
        for book in dataset:
            if not self.__check_existance(book['book_id']):
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

    def __get_all_ids(self):
        book_ids = []

        books = Book.query.all()

        for book in books:
            book_ids.append(book.book_id)

        return book_ids

    def get_all_books(self):
        quantity = 0
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



    def __date_processor(self, published_date):
        date = published_date.split("-")

        if len(date) == 3:
            return [date[0], date[1], date[2]]
        elif len(date) == 2:
            return [date[0], date[1], None]
        elif len(date) == 1:
            return [date[0], None, None]





    def __asign_with_authors(self, book_id, authors):
        book = self.__get_book_by_id(book_id)

        for author in authors:
            book.authors.append(author)

        db.session.commit()

    def __asign_with_categories(self, book_id, categories):
        book = self.__get_book_by_id(book_id)

        for category in categories:
            book.categories.append(category)

        db.session.commit()

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
        self.raw = self.__get_book_by_id(book_id)

        if self.raw:
            return True

        return False

    def __get_names(self, iterable_obj):
        buffer = []

        for obj in iterable_obj:
            buffer.append(obj.name)

        return buffer

    def __get_date_str(self, book):
        date = ""

        def less_than_ten(num):
            if num < 10:
                return "0" + str(num)

        if not book.published_day and not book.published_month and book.published_year:
            date = str(book.published_year)
        elif not book.published_day and  book.published_month and book.published_year:
            date = str(book.published_year) + "-" + less_than_ten(book.published_month)
        else:
            date = str(book.published_year) + "-" + str(book.published_month) + "-" + str(book.published_day)

        return date

    def __add_book(self, new_book_obj):
        db.session.add(new_book_obj)

    def __get_book_by_id(self, book_id):
        return Book.query.filter_by(book_id=book_id).first()

    def __commit_dataset(self):
        db.session.commit()
        db.session.remove()
        db.session.close()


class Authors_manager(Author):

    def add_authorship(self, dataset):
        dataset_processed = dataset
        books_counter = 0
        authors_counter = 0

        for book in dataset_processed:
            book['authors'] = book['authors'] if book['authors'] else []
            for author in book['authors']:
                if self.__check_existance(author):
                    author_obj = deepcopy(self.raw)
                    dataset_processed[books_counter]['authors'][authors_counter] = author_obj
                else:
                    author_obj = Author(name = author)

                    db.session.add(author_obj)
                    self.__commit()
                    self.__check_existance(author)
                    author_obj = deepcopy(self.raw)
                    dataset_processed[books_counter]['authors'][authors_counter] = author_obj


                authors_counter += 1

            books_counter += 1
            authors_counter = 0

        return dataset_processed


    def __check_existance(self, name):
        self.raw = Author.query.filter_by(name=name).first()

        if self.raw:
            return True

        return False

    def __commit(self):
        db.session.commit()
        db.session.remove()
        db.session.close()

class Categories_manager(Category):

    def add_category_affiliation(self, dataset):
        dataset_processed = dataset
        books_counter = 0
        categories_counter = 0

        for book in dataset_processed:
            book['categories'] = book['categories'] if book['categories'] else []
            for category in book['categories']:
                if self.__check_existance(category):
                    category_obj = deepcopy(self.raw)
                    dataset_processed[books_counter]['categories'][categories_counter] = category_obj
                else:
                    category_obj = Category(name = category)

                    db.session.add(category_obj)
                    self.__commit()
                    self.__check_existance(category)
                    category_obj = deepcopy(self.raw)
                    dataset_processed[books_counter]['categories'][categories_counter] = category_obj


                categories_counter += 1

            books_counter += 1
            categories_counter = 0

        return dataset_processed


    def __check_existance(self, name):
        self.raw = Category.query.filter_by(name=name).first()

        if self.raw:
            return True

        return False

    def __commit(self):
        db.session.commit()
        db.session.remove()
        db.session.close()



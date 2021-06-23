from app import app, api, db
from db_manager import Books_manager, Authors_manager, Categories_manager
from werkzeug.datastructures import ImmutableDict
from googleapis_books import BooksExplorer
from flask_restful import Resource, reqparse, abort
from flask import request

#post params registration
book_post_args = reqparse.RequestParser()
book_post_args.add_argument('q', type=str, help="hi parameter is required!", required=True)

#/book/<book_id> method. Returns book by book_id (not database increment id!!!)
class GetBook(Resource):
    def get(self, book_id):
        book = Books_manager()
        book.load_book(book_id = book_id)

        return book.get_book_dict()

#/book - returns list of all books
#/book?author="author_name_one"&author="author_name_two" - returns list of
class GetAllBooks(Resource):
    def get(self):
        dict = request.args
        dict = dict.to_dict(flat=False)
        response = []
        quantity = 0

        if 'author' in dict.keys():
            authors = dict['author']

            for author_name in authors:
                authors_manager = Authors_manager()
                book_ids = authors_manager.get_authors_books_ids(author_name.replace("'","").replace('"',""))

                if not book_ids:
                    abort(404, message="Books with author={} does not exist".format(author_name.replace("'","").replace('"',"")))

                books_manager = Books_manager()
                books = books_manager.get_all_books(book_ids)

                for book in books['books']:
                    response.append(book)

                quantity += int(books['quantity'])

            return {
                "quantity": quantity,
                "books": response
            }

        elif 'sort' in dict.keys():
            book_manager = Books_manager()

            if dict['sort'][0] == '+published_date':
                books = book_manager.get_books_by_year(order="+")
                return books
            else:
                books = book_manager.get_books_by_year(order="-")
                return books

        elif 'published_date' in dict.keys():
            book_manager = Books_manager()
            books = book_manager.get_books_by_year(year=dict['published_date'][0])
            return books

        else:
            book = Books_manager()

            return book.get_all_books()

#/db method. Adds datasets to the database
class Db(Resource):
    def post(self):
        args = book_post_args.parse_args()

        #database fetching
        explorer = BooksExplorer()
        dataset = explorer.get_dataset(args.q)

        #adding authors
        authors = Authors_manager()
        dataset = authors.add_authorship(dataset)

        #adding categories
        categories = Categories_manager()
        dataset = categories.add_category_affiliation(dataset)

        #commiting dataset
        book = Books_manager()
        book.add_dataset(dataset)


        return {
            'message': args.q
        }

api.add_resource(GetAllBooks, "/book")
api.add_resource(GetBook, "/book/<book_id>")
api.add_resource(Db, '/db')

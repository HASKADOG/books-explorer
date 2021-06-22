from app import app, api, db
from books_db_manager import Books_manager, Authors_manager, Categories_manager
from googleapis_books import BooksExplorer
from flask_restful import Resource, reqparse

book_post_args = reqparse.RequestParser()
book_post_args.add_argument('q', type=str, help="hi parameter is required!", required=True)

class GetBook(Resource):
    def get(self, book_id):

        book = Books_manager()
        book.load_book(book_id = book_id)

        return book.get_book_dict()

class GetAllBooks(Resource):
    def get(self):
        book = Books_manager()

        return book.get_all_books()

class Db(Resource):
    def post(self):
        args = book_post_args.parse_args()

        explorer = BooksExplorer()
        dataset = explorer.get_dataset(args.q)

        authors = Authors_manager()
        dataset = authors.add_authorship(dataset)

        categories = Categories_manager()
        dataset = categories.add_category_affiliation(dataset)

        book = Books_manager()
        book.add_dataset(dataset)


        return {
            'message': args.q
        }
api.add_resource(GetAllBooks, "/book")
api.add_resource(GetBook, "/book/<book_id>")
api.add_resource(Db, '/db')
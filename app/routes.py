from app import app, api, db
from books_db_manager import Book
from flask_restful import Resource, reqparse

book_post_args = reqparse.RequestParser()
book_post_args.add_argument('q', type=str, help="hi parameter is required!", required=True)

class GetBook(Resource):
    def get(self, book_id):
        book = Book(book_id=book_id)

        return book.get_book_dict()

class Db(Resource):
    def post(self):
        args = book_post_args.parse_args()

        return {
            'message': args
        }

api.add_resource(GetBook, "/book/<book_id>")
api.add_resource(Db, '/db')
import requests

class BooksExplorer():

    def __init__(self):
        print('...BooksExplorer initiated...')

    def add_dataset(self, q):
        dataset = self.__get_dataset(q)

        return self.__decompose_books(dataset)

    def __get_dataset(self, q):
        dataset = requests.post(url='https://www.googleapis.com/books/v1/volumes', params={'q': q}).json()

    def __decompose_books(self, dataset):
        books = []

        for book in dataset['items']:
            books.append({
                'book_id': book['id'] if book['id'] else None,
                'title': book['volumeInfo']['title'] if book['volumeInfo']['title'] else None,
                'authors': book['volumeInfo']['authors'] if book['volumeInfo']['authors'] else None,
                'categories': book['volumeInfo']['categories'] if book['volumeInfo']['categories'] else None,
                'published_date': book['volumeInfo']['publishedDate'] if book['volumeInfo']['publishedDate'] else None,
                'average_rating': book['volumeInfo']['averageRating'] if book['volumeInfo']['averageRating'] else None,
                'ratings_count': book['volumeInfo']['ratingsCount'] if book['volumeInfo']['ratingsCount'] else None,
                'thumbnail': book['volumeInfo']['imageLinks']['thumbnail'] if book['volumeInfo']['imageLinks'][
                    'thumbnail'] else None,
            })

        return books


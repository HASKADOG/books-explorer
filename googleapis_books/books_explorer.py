import requests, copy

class BooksExplorer():

    #dataset pattern
    book_properties = {
            'book_id': ['id'],
            'title': ['volumeInfo', 'title'],
            'authors': ['volumeInfo', 'authors'],
            'categories': ['volumeInfo', 'categories'],
            'published_date': ['volumeInfo', 'publishedDate'],
            'average_rating': ['volumeInfo', 'averageRating'],
            'ratings_count': ['volumeInfo', 'ratingsCount'],
            'thumbnail': ['volumeInfo', 'imageLinks', 'thumbnail']
        }

    #returns loaded dataset for further manipulations
    def get_dataset(self, q):
        dataset = self.__get_dataset(q)

        return self.__decompose_books(dataset)

    #fetches dataset from google books api
    def __get_dataset(self, q):
        return requests.get(url='https://www.googleapis.com/books/v1/volumes', params={'q': q}).json()

    #decomposes books from JSON
    def __decompose_books(self, dataset):
        books = []

        for book in dataset['items']:
            books.append(self.__get_checked_props(book))

        return books

    #checks if property in JSON
    def __get_checked_props(self, item):
        props = copy.deepcopy(self.book_properties)

        for key, value in props.items():
            try:
                if len(value) == 1:
                    props[key] = item[value[0]]
                elif len(value) == 2:
                    props[key] = item[value[0]][value[1]]
                elif len(value) == 3:
                    props[key] = item[value[0]][value[1]][value[2]]
            except:
                props[key] = None

        return props


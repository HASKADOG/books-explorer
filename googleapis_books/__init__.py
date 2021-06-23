#                         _                  _       _                 _
#                        | |                (_)     | |               | |
#  __ _  ___   ___   __ _| | ___  __ _ _ __  _ ___  | |__   ___   ___ | | _____
# / _` |/ _ \ / _ \ / _` | |/ _ \/ _` | '_ \| / __| | '_ \ / _ \ / _ \| |/ / __|
# | (_| | (_) | (_) | (_| | |  __/ (_| | |_) | \__ \ | |_) | (_) | (_) |   <\__ \
# \__, |\___/ \___/ \__, |_|\___|\__,_| .__/|_|___/ |_.__/ \___/ \___/|_|\_\___/
#  __/ |             __/ |            | |       ______
# |___/             |___/             |_|      |______|


"""
GoogleApis Books Explorer
~~~~~~~~~~~~~~~~~~~~~

Properties:
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
    e.g:
        'title'(name of the property) : ['volumeInfo', 'title'](JSON path)


"""

from .books_explorer import BooksExplorer

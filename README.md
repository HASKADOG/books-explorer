Test assignment for STXnext |
Author: Ramazan Safiullun |
Phone: +48-575-047-127 

Link to the application: https://ramazan.tech/books-explorer/v1/

How to run
1) python3 -m venv venv.
2) pip install -r requirements.txt
3) source venv/bin/activate
4) export FLASK_APP=books_explorer.py
5) flask run
5.1) If you have your server and you want to use it not only in your localhost, use "flask run --host="0.0.0.0"
If you want to deploy it as I did, use this guide: https://www.youtube.com/watch?v=goToXTC96Co&t=4015s

Methods
1) GET /book - returns list of all books
2) GET /book/<book_id> - return book with certain id
3) GET /book?sort=-published_date - returns list of books sortde by years in descending order
4) GET /book?sort=%2Bpublished_date - returns list of books sorted by years in ascending order. I suggest to use %2B instead of + because of the encoding.
5) GET /book?published_year=<year> - returns list of books that was published in certain year
6) GET /book?author=<name_one>&author=<name_two> - returns list of books assigned with certain authors. Here's can be any quantity of authors
7) POST /db with body {"q":"Hobbit"} - loads and writes new dataset to the application. If finished successfully, returns JSON with used query.

DataBase architecture

![image](https://user-images.githubusercontent.com/27897422/123192491-52de7300-d4a3-11eb-837d-c5b358f6cd01.png)



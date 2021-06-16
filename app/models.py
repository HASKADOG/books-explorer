from app import db

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    published_date = db.Column(db.Date)
    average_rating = db.Column(db.Integer)
    ratings_count = db.Column(db.Integer)
    thumbnail = db.Column(db.String(512))
    authors_junction = db.relationship('AuthorsJunction', backref='authors', lazy='dynamic')
    categories_junction = db.relationship('CategoriesJunction', backref='categories', lazy='dynamic')

    def __repr__(self):
        return '<Book {}>'.format(self.title)

class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    authors_junction = db.relationship('AuthorsJunction', backref='author', lazy='dynamic')


    def __repr__(self):
        return '<Author {}>'.format(self.name)

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    categories_junction = db.relationship('CategoriesJunction', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)

class AuthorsJunction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return '<AuthorsJunction book_id:{} author_id:{}>'.format(self.book_id, self.author_id)

class CategoriesJunction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return '<CategoriesJunction book_is:{} author_id:{}>'.format(self.book_id, self.category_id)
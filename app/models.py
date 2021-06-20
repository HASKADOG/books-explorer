from app import db

authorship = db.Table(
    'authorship',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
    )

category_affilation = db.Table(
    'category_affilation',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String(32), unique=True)
    title = db.Column(db.String(128))
    published_day = db.Column(db.Integer)
    published_month = db.Column(db.Integer)
    published_year = db.Column(db.Integer)
    average_rating = db.Column(db.Integer)
    ratings_count = db.Column(db.Integer)
    thumbnail = db.Column(db.String(512))
    authors = db.relationship('Author', secondary=authorship, backref=db.backref('books', lazy='dynamic'))
    categories = db.relationship('Category', secondary=category_affilation, backref=db.backref('books', lazy='dynamic'))

    def __repr__(self):
        return '<Book {}>'.format(self.title)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return '<Author {}>'.format(self.name)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return '<Category {}>'.format(self.name)
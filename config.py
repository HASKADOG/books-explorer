import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DATABASE_NAME = 'books_explorer'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, DATABASE_NAME + '.db?check_same_thread=False')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
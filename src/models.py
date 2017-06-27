# This is the creation of the database for the listing of the Books as descirbed
# in the UDM.  This database is created using the tools for SQL Alchemy to create
# a database in sqlite.

# sqlalchemy imports needed to create the database.
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from controllers import connect_to_db
from app import login_session

Base = declarative_base()
session = connect_to_db()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    picture = Column(String)

    def __init__(self, name, email, picture):
        self.name = name
        self.email = email
        self.picture = picture

    @classmethod
    def create_user(cls, login_session):
        new_user = User(name=login_session['username'],
                        email=login_session['email'],
                        picture=login_session['picture'])
        session.add(new_user)
        session.commit()
        user = session.query(User).filter_by(
            email=login_session['email']).one()
        return user.id

    @classmethod
    def get_user_info(cls, user_id):
        print login_session['email']
        try:
            user = session.query(User).filter_by(id=user_id).one()
            return user
        except:
            return None

    @classmethod
    def get_current_user(cls):
        try:
            print login_session['email']
            return get_user_info(get_user_id(login_session['email']))
        except:
            return 'Guest'

    @classmethod
    def get_user_id(cls, user_email):
        try:
            user = session.query(User).filter_by(email=self.email).one()
            print user.id
            return user.id
        except:
            return None


class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    language = Column(String, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'language': self.name
        }

    def __init__(self, language=None):
        self.language = language

    @classmethod
    def get_languages(cls):
        return session.query(Language).all()

    @classmethod
    def get_book_language(cls, language_id):
        return session.query(Book).filter_by(id=language_id).all()


class Book(Base):
    __tablename__ = 'Books'

    id = Column(Integer, primary_key=True)
    book_img = Column(String)
    book_title = Column(String(80))
    book_author = Column(String(80))
    book_description = Column(String)

    language_id = Column(Integer, ForeignKey('language.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    language = relationship(Language)

    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'book_img': self.book_img,
            'book_title': self.book_title,
            'book_author': self.book_author,
            'book_descirption': self.book_description,
            'book_url': self.book_url,
            'language_id': self.language_id,
            'user_id': self.user_id
        }

    @classmethod
    def get_books(cls):
        return session.query(Book).order_by(Book.book_title).all()

    @classmethod
    def get_book(cls, book_id):
        return session.query(Book).filter_by(id=book_id).one()

    def __init__(self, book_img=None, book_title=None, book_author=None,
                 book_description=None, book_url=None, language_id=None,
                 user_id=None):
        self.book_img = book_img
        self.book_title = book_title
        self.book_author = book_author
        self.book_description = book_description
        self.book_url = book_url
        self.language_id = language_id
        self.user_id = user_id


class Review(Base):
    __tablename__ = reviews

    id = Column(Integer, primary_key=True)
    review = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    book_id = Column(Integer, ForeignKey('book.id'))
    user = relationship(User)
    book = relationship(Book)

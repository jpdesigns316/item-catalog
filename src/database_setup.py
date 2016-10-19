# This is the creation of the database for the listing of the books as descirbed
# in the UDM.  This database is created using the tools for SQL Alchemy to create
# a database in sqlite.

# sqlalchemy imports needed to create the database.
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    def __init__(self, name, email, picture):
        self.name = name
        self.email = email
        self.picture = picture

class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    language = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'language': self.name
        }


    def __init__(self, language=None):
        self.language = language

# Future implementation code for creation of prices of books
# class BookPrice(Base):
#     __tablename__ = 'book_price'
#
#     id = Column(Integer, primary_key=True)
#     book_id = Column(String, ForeignKey('books.id'))
#     book = relationship("Book", foreign_keys=['book_id'])
#     price = Column(String(8))
#     url = Column(String(250))
#
#     @property
#     def serialize(self):
#         return {
#             'id': self.id,
#             'book_id': self.book_id,
#             'price': self.price,
#             'url': self.url
#         }


class Books(Base):
    __tablename__ = 'books'


    id = Column(Integer, primary_key=True)
    book_img = Column(String(250))
    book_title = Column(String(80))
    book_author = Column(String(80))
    book_description = Column(String(250))
    book_url = Column(String(250))
    # book_price_id = Column(Integer, ForeignKey('book_price.id'))
    language_id = Column(Integer, ForeignKey('language.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    language = relationship(Language)
    # book_price = relationship(BookPrice)
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





engine = create_engine('postgresql://catalog:Bradycheated@localhost/catalog')


Base.metadata.create_all(engine)

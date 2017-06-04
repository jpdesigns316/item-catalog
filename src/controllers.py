from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Books, User, Language

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']


def connect_to_db():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


session = connect_to_db()


def create_user(login_session):
    new_user = User(name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Funtion that will retrieve information form the User model based upon the
# user_id and return information about the user.
def get_user_info(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except:
        return None


# This function will retrieve infromation abouthe used based on the
# email given. If there is no record in the database then it will return
# None.
def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Following functions contain querys that are used at multiple instances
# thoughout the blueprint. They are in place so you do not have to changes
# each instance, but make things easier to do.

# Query fucntion that will return the list of books in alphabetical order
def get_books():
    return session.query(Books).order_by(Books.book_title).all()


# Query fuction that will return the languages in the Language model
def get_languages():
    return session.query(Language).all()


# Utilized the functions in app to get the user infromation and uses that
# to display that information in the template. Though the username is
# currently used, this could be helpful for future modifation of information
# that is displayed about the user
def get_current_user():
    return get_user_info(get_user_id(login_session['email']))


# Query function that returns information about the book_id given.
def get_book(book_id):
    return session.query(Books).filter_by(id=book_id).one()


# Query function that returns information about the language_id given.
# This helps to display only books in that language
def get_book_language(language_id):
    return session.query(Books).filter_by(language_id=language_id).all()

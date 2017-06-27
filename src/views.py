from flask import Blueprint, Flask, render_template, request, redirect, \
    url_for, jsonify

# Database model
from functools import wraps
from forms import BookForm
from sqlalchemy import desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from flask import session as login_session
import controllers as c
import random
import string

session = c.connect_to_db()

books_blueprint = Blueprint('books', __name__)


# Function returned to the user when they try to modify a book that they
# did not create


def user_error():
    return "<script>function modifyBook(){ alert('You are only not authoized to "\
           "modify this book. Please create your own book creation.');" \
           "window.location='/books/add/book'}</script><body onload='modifyBook()'>"


@books_blueprint.route('/')
def index():
    if 'username' in login_session:
        return render_template('books.jinja2',
                               books=models.Book.get_books(),
                               languages=models.Language.get_languages(),
                               user=c.get_current_user())
    # This creates a random string of information that will be used in the
    # thrid-party authentication.
    return render_template('books.jinja2',
                           books=models.Book.get_books(),
                           languages=models.Language.get_languages(),
                           STATE=c.make_state())


@books_blueprint.route('/add/book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if request.method == 'POST' and form.validate():
        books = session.query(models.Books).all()
        # Creating a books object to add to the databse.
        book = Books(book_img=request.form['book_img'],
                     book_title=request.form['book_title'],
                     book_author=request.form['book_author'],
                     book_description=request.form['book_description'],
                     book_url=request.form['book_url'],
                     language_id=request.form['language_id'],
                     user_id=login_session['user_id'])
        session.add(book)
        session.commit()
        return redirect(url_for('books.index'))
    else:
        return render_template('add_book.jinja2',
                               languages=c.get_languages(),
                               form=form,
                               user=c.get_current_user())


@books_blueprint.route('/delete/<int:book_id>', methods=['GET', 'POST', 'DELETE'])
def delete_book(book_id):
    if get_book(book_id) != login_session['user_id']:
        return user_error()
    if request.method == 'POST':
        session.delete(get_book(book_id))
        session.commit()
        return redirect(url_for('books.index', books=get_books()))
    else:
        return render_template('delete_book.jinja2',
                               books=c.get_book(book_id),
                               languages=c.get_languages(),
                               user=c.get_current_user())


@books_blueprint.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if 'username' not in login_session:
        return redirect('/books')
    editedBook = session.query(models.Book).filter_by(id=book_id).one()
    user = c.get_current_user()

    if editedBook.user_id != login_session['user_id']:
        return user_error()
    if user.id == editedBook.user_id:
        if request.method == 'POST':
            editedBook.book_img = request.form['book_img']
            editedBook.book_title = request.form['book_title']
            editedBook.book_author = request.form['book_author']
            editedBook.book_description = request.form['book_description']
            editedBook.book_url = request.form['book_url']
            editedBook.language_id = request.form['language_id']

            session.add(editedBook)
            session.commit()
            return redirect(url_for('books.index'))
        else:
            return render_template('edit_book.jinja2',
                                   book=c.get_book(book_id),
                                   languages=c.get_languages(),
                                   user=c.get_current_user())


@books_blueprint.route('/language/<int:language_id>')
def get_language_page(language_id):
    if 'username' in login_session:
        return render_template('books.jinja2',
                               books=c.get_book_language(language_id),
                               languages=c.get_languages(),
                               user=c.get_current_user())
    return render_template('books.jinja2',
                           books=c.get_book_language(language_id),
                           languages=c.get_languages(),
                           user='Guest',
                           STATE=c.make_state())


# JSON API's to display infromation about the books
@books_blueprint.route('/JSON')
def books_json():
    books = c.get_books()
    return jsonify(books=[book.serialize for book in books])


@books_blueprint.route('/<int:book_id>/JSON')
def book_json(book_id):
    book = c.get_book(book_id)
    return jsonify(books=book.serialize)

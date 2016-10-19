 # Copyright 2016 Jpdesigns316. All rights reserved.
 #
 # Redistribution and use in source and binary forms, with or without
 # modification, are permitted provided that the following conditions are
 # met:
 #
 #    * Redistributions of source code must retain the above copyright
 # notice, this list of conditions and the following disclaimer.
 #    * Redistributions in binary form must reproduce the above
 # copyright notice, this list of conditions and the following disclaimer
 # in the documentation and/or other materials provided with the
 # distribution.
 #    * Neither the name of Google Inc. nor the names of its
 # contributors may be used to endorse or promote products derived from
 # this software without specific prior written permission.
 #
 # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 # "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 # LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 # A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 # OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 # SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 # LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 # DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 # THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 # (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 # OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from flask import Flask, render_template, request, make_response, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Books, Language


from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests


app = Flask(__name__)
app.secret_key = 'rF&UM39t6Rn2S6422776H9e3!*5D62*K'

engine = create_engine('postgresql://catalog:Bradycheated@localhost/catalog')
Base.metadata.bind = engine

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    return render_template('welcome.jinja2')

# The following functions (gconnect, gdisconnect) help with the thrid-party
# connections with Google Plus authentication. They are in place to obtain
# information about that user from ther google account and use it in conjuction
# with interating with the website.
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != app.config['CLIENT_ID']:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('User not logged in'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        return redirect('/books')
    else:
        # response = make_response(json.dumps("Failed to logout"), 400)
        # response.headers['Content-Type'] = 'application/json'
        return render_template("logout_error.html")

# This function will create a new user in the database. Based upon the
# information from the login_session is will store it. This is done
# so there could not be duplicate emails
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
    user = session.query(User).filter_by(id=user_id).one()
    return user

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

# Function returned to the user when they try to modify a book that they did not create
def user_error():
    return "<script>function modifyBook(){ alert('You are only not authoized to "\
           "modify this book. Please create your own book creation.');" \
           "window.location='/books/add/book'}</script><body onload='modifyBook()'>"

@app.route('/')
def index():
    if 'username' in login_session:
        return render_template('books.jinja2',
                                books=get_books(),
                                languages=get_languages(),
                                user=get_current_user())
    # This creates a random string of information that will be used in the
    # thrid-party authentication.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('books.jinja2',
                            books=get_books(),
                            languages=get_languages(),
                            STATE=state)

@app.route('/add/book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        books = session.query(Books).all()
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
                                languages=get_languages(),
                                user=get_current_user())

@app.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    if get_book(book_id) != login_session['user_id']:
        return user_error()
    if request.method == 'POST':
            session.delete(get_book(book_id))
            session.commit()
            return redirect(url_for('books.index',books=get_books()))
    else:
        return render_template('delete_book.jinja2',
                                books=get_book(book_id),
                                languages=get_languages(),
                                user=get_current_user())

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if 'username' not in login_session:
        return redirect('/books')
    editedBook = session.query(Books).filter_by(id=book_id).one()
    user = get_current_user()

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
                                    book=get_book(book_id),
                                    languages=get_languages(),
                                    user=get_current_user())


@app.route('/language/<int:language_id>')
def get_language_page(language_id):
    if 'username' not in session:
        render_template('books.jinja2',
                        books=get_book_language(language_id),
                        languages=get_languages())
    return render_template('books.jinja2',
                    books=get_book_language(language_id),
                    languages=get_languages(),
                    user=get_current_user())


# JSON API's to display infromation about the books
@app.route('/JSON')
def books_json():
    books = get_books()
    return jsonify(books=[book.serialize for book in books])

@app.route('/<int:book_id>/JSON')
def book_json(book_id):
    book = get_book(book_id)
    return jsonify(books=book.serialize)


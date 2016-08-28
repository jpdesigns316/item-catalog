![Programming by Reading] (src/static/image/logo2.png)

This is the fourth full coding project which was completed under the Full Stack Web Designer
for the Udacity nanodegree. It's purpose was to create an item catalog based the field which
the user has chosen. The orignal lesson given was a Restaurant Menu Database. Through the
lessons the design was expounded and given a new form.

Programming by Reading is meant to be a database of programming books that could be helpful
to people who want to learn coding. Possible additions could be setting up so the users can 
review the books, also have a section on why the book  is useful.

This program utilizes a two-level security system to prevent users from accessing material
that they did not create.
1. Client Level - This is the code specifically written in the jinja code that will do
security checks to make sure that parts of the website are only accessible to the owners
of the books.
2. Code Level - In addition to the security that was written in the jinja code, there is
also code that requires a user to be logged in to have access to certain methods. If, by
chance, a user bypasses the first level they would get error messages letting them know
that they could not modify it.

## Installation

1.  [Python 2.7] (https://www.python.org/downloads/release/python-2712/) - Code the software was designed in.
2.  Git Account - This would be need to download the repository either through using 'git clone' or by downloading this as a zip.
3.  Google Account - To test out the Google+ third-party sign in.


### Step One

Get the repository from github:
```
$ git clone https://github.com/jpdesigns316/item-catalog item-catalog
```
or Go to the [repository](https://github.com/jpdesigns316/item-catalog) on GitHub and click on the 'Clone or download' button. Unzip into a directory called item-catalog.

### Step Two

**Setup Google Plus Authentication Application**

1.  Go to https://console.developers.google.com/project and login with Google.
2.  Create a new project
3.  Name the project
4.  Select "API's and Auth-> Credentials-> Create a new OAuth client ID" from the project menu
5.  Select Web Application
6.  On the consent screen, type in a product name and save.
7.  In Authorized javascript origins add: http://localhost:5000, In Authroized redirect URI add: http://localhost:5000/login http://localhost:5000/gconnect
8.  Click create client ID
9.  Click download JSON and save it into the root director of this project.
10. Rename the JSON file "client_secret.json"
11. In the installation menu you can setup with your client id.

### Step Three

A installation menu has been created to help get this program configured
```
C:\%PATH_TO_CODE%\src\python runme.py
```
* * *  
## Routes

Route | Function | Description
---|---|---
/ | home() | Brings up the landing page of the website.
/login | show_login() | Render login.jinja2 page that lets the user login.
/gconnect | gconnect() |Allows the user to login to the website by using Google Plus.
/gdisconnect | gdisconnect() | Allows the user to disconnect from Google Plus.

* * *  

## Files
File | Desciption
---|---
_src/app.py_   | Project code containing code for the connection to thrid party sites
_src/database_setup.py_  |Contains the model used in the database, and serializes them into JSON via __init__.
_src/add_books_to_db.py_ | Set of default books used to add to the database for testing
_src/client_secrets.json_  | This is used for the connection of third party authentication
_src/config.py_ | Contains configuration information in the from of constants used in the program.
_src/requirements.txt_|The requirements of different Python modules not included in the base installation
_src/run.py_|Runs the webserver based on the infromation in app.py and the constants from config.py|_src/utils.py_
Helper functions used to help keeping things simple. |
_src/views/books.py_ | Blueprint used in the routes used to create the endpoints.
_src/templates_ |Directory of the template files in jinja2 format to let the user know that jinja2 template format is being used.
_src/static_ | Directory holding the static files for js, css, images, and fonts

* * *

## Files and their functions

_app.py_  
File | Desciption
---|---
_create_user(login_session)_ | Creates a user base on the infromation in the login_session.
_get_user_id(email)_ | Look up the user id via the email that was accessed throught the thrid-party authentication.
_get_user_info(user_id)_ | Get the user informaton from the User model after finding out the user_id


## books.py Bleuprints

Route | Function | Description
---|---|---
_books_ | home() | Brings up the landing page of the books.
_add/book_ | add_book() | Utilizes the methond **GET** and **POST** to add a book to the database based upon the data in the Books model
_delete/<int:book_id>_ | delete_book() | Removes a books for the database
_books/<int:language_id>_ | get_language_page() | Will only list the books depending on the language_id

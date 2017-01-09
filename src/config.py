# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
import json
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

ADMIN = frozenset(["admin"])
IP_ADDRESS = '0.0.0.0'
PORT=5000
SECRET_KEY = 'rF&UM39t6Rn2S6422776H9e3!*5D62*K'

# Defining the database
DATABASE_NAME = 'books.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)
DATABASE_CONNECT_OPTIONS = {}

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Programming by Reading"

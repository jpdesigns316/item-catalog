from flask import Blueprint

languages_blueprint = Blueprint('books', __name__)

@languages_blueprint.route('/')
def c_plus_plus():
    pass


def java():
     pass


def js():
    pass


def php():
    pass


def python():
    pass


def ruby():
    pass

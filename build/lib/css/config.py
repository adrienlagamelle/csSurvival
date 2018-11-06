import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # General Info
    TITLE = 'csSurvival'
    COPYRIGHT = (
        '© 2018 Adrien Lagamelle, Daniel Power, '
        'Kent Barter, Stephen Walsh, Xuemeng Li'
    )

    # Security Keys
    # NOTE Ensure secure Secret Key and CSRF Token set for final deployment
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-string'
    CSRF_TOKEN = os.environ.get('CSRF_TOKEN') or 'another-string'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    WHOOSH_BASE = os.path.join(basedir, 'search.db')

    MAX_SEARCH_RESULTS = 50

    DEBUG = True

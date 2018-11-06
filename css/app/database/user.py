"""Interface for the User table of the database"""

from datetime import datetime
from . import sqlalchemy
from .models import User


def new(username, email, password):
    """Add a new user to the database

    Args:
        username (str): The username for the user (must be unique)
        email (str): The email address for the user (must be unique)
        password (str): The password for the user

    Returns:
        obj: Instance of User
    """
    user = User(username=username, email=email)
    user.set_password(password)
    sqlalchemy.session.add(user)
    sqlalchemy.session.commit()

    return user


def get(id):
    """Retrieve a user from the database

    Args:
        id (int): The id of the user you wish to retreive

    Returns:
        obj: Instance of User
    """

    return User.query.get(id)


def getFromEmail(email):
    """Retreive a user given its email address

    Args:
        email (str): The email address of the desired user

    Returns:
        obj: Instance of User
    """

    return User.query.filter_by(email=email).first()


def getFromUsername(username):
    """Retreive a user given its username

    Args:
        username (str): The username of the desired user

    Returns:
        obj: Instance of User
    """

    return User.query.filter_by(username=username).first()


def getAll():
    """Retreive all users

    Returns:
        list (Instance of User): A list of all users in the database
    """

    return User.query.all()


def update(user_id, username=None, about=None, language=None):
    """Edit attributes of the user with the given id

    Args:
        user_id (int): The id of the user you wish to edit
        username (str): The new username of the user (must be unique)
        about (str): The user's about text (shown on profile)
        language (str): The user's preferred language ("en" or "fr")
    """

    user = get(user_id)
    if username is not None:
        user.username = username
        sqlalchemy.session.commit()
    if about is not None:
        user.about = about
        sqlalchemy.session.commit()
    if language is not None:
        user.language = language
        sqlalchemy.session.commit()


def updateActivity(user_id):
    """Update the user's "last active" time

    Args:
        user_id (int): The id of the user whose activity is being updated
    """

    user = get(user_id)
    user.last_seen = datetime.utcnow()
    sqlalchemy.session.commit()

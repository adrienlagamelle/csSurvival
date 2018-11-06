"""Interface for the Thread table of the database"""

from . import sqlalchemy
from .models import Thread


def new(title, body, user_id, group_id=None):
    """Add a new thread to the database

    Args:
        title (str): The title of the new thread
        body (str): Body text of the new thread (may contain markdown)
        user_id (int): The id of the thread's author
        group_id (int): The id of the group containing the thread

    Returns:
        obj: Instance of Thread
    """

    thread = Thread(
        title=title,
        body=body,
        user_id=user_id,
        group_id=group_id
    )
    sqlalchemy.session.add(thread)
    sqlalchemy.session.commit()

    return thread


def get(id):
    """Retrieve a thread from the database

    Args:
        id (int): The id of the thread you wish to retreive

    Returns:
        obj: Instance of Thread
    """

    return Thread.query.get(id)


def getAll():
    """Retreive all threads

    Returns:
        list (Instance of Thread): A list of all threads in the database
    """

    return Thread.query.all()


def search(string):
    """Retreive all threads containing the given string in their title or body

    Args:
        string (str): The string you wish to match

    Returns:
        list (Instance of Thread): A list of threads matching the given string
    """

    return Thread.query.whoosh_search(string).all()


def update(thread_id, title=None, group_id=None, body=None):
    """Edit attributes of the thread with the given id

    Args:
        thread_id (int): The id of the thread you wish to edit
        title (str): The title of the thread
        body (str): The body content of the thread (may contain markdown)
        group_id (int): The id of the group containing the thread
    """

    thread = get(thread_id)
    if title:
        thread.title = title
    if group_id:
        thread.group_id = group_id
    if body:
        thread.body = body
    if group_id:
        thread.group_id = group_id

    sqlalchemy.session.add(thread)
    sqlalchemy.session.commit()


def delete(id):
    """Remove a thread from the database

    Args:
        id (int): The id of the thread you wish to remove
    """

    thread = Thread.query.get(id)
    sqlalchemy.session.delete(thread)
    sqlalchemy.session.commit()

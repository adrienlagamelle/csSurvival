"""Interface for the Comment table of the database"""

from . import sqlalchemy
from .models import Comment


def new(body, user_id, thread_id):
    """Add a new comment to the database

    Args:
        body (str): The contents of the comment
        user_id (int): The id of the post's author
        thread_id (int): The id of the thread which contains the comment

    Returns:
        obj: Instance of Comment
    """

    comment = Comment(body=body, user_id=user_id, thread_id=thread_id)
    sqlalchemy.session.add(comment)
    sqlalchemy.session.commit()

    return comment


def get(comment_id):
    """Retrieve a comment from the database

    Args:
        id (int): The id of the comment you wish to retreive

    Returns:
        obj: Instance of Comment
    """

    return Comment.query.get(comment_id)


def delete(id):
    """Remove a comment from the database

    Args:
        id (int): The id of the comment you wish to remove
    """

    comment = Comment.query.get(id)
    sqlalchemy.session.delete(comment)
    sqlalchemy.session.commit()

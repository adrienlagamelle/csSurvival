"""Interface for the Subscription table of the database"""

from . import sqlalchemy
from .models import Subscription


def new(user_id, thread_id):
    """Add a new subscription to the database

    Args:
        user_id (int): The id of the subscribing user
        thread_id (int): The id of the thread being subscribed to

    Returns:
        obj: Instance of Subscription
    """

    subscription = Subscription(
        user_id=user_id,
        thread_id=thread_id,
    )
    sqlalchemy.session.add(subscription)
    sqlalchemy.session.commit()

    return subscription


def get(id):
    """Retrieve a subscription from the database

    Args:
        id (int): The id of the subscription you wish to retreive

    Returns:
        obj: Instance of Subscription
    """

    return Subscription.query.get(id)


def getFromMembers(user_id, thread_id):
    """Retreive a subscription given the ids of the subscriber and thread

    Args:
        user_id (int): The id of the user subscribing user
        thread_id (int): The id of the thread being subscribed to

    Returns:
        obj: Instance of Subscription
    """

    sub = Subscription.query.filter_by(
        user_id=user_id,
        thread_id=thread_id
    ).first()

    return sub


def delete(user_id, thread_id):
    """Remove a subscription from the database

    Args:
        id (int): The id of the subscription you wish to remove
    """

    subs = Subscription.query.filter_by(
        user_id=user_id,
        thread_id=thread_id
    )

    for sub in subs:
        sqlalchemy.session.delete(sub)
        sqlalchemy.session.commit()

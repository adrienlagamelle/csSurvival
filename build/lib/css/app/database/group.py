"""Interface for the Group table of the database"""

from . import sqlalchemy
from .models import Group
from .models import User


def new(name):
    """Add a new group to the database

    Args:
        name (str): The name of the group

    Returns:
        obj: Instance of Group
    """

    group = Group(name=name)
    sqlalchemy.session.add(group)
    sqlalchemy.session.commit()

    return group


def get(id):
    """Retrieve a group from the database

    Args:
        id (int): The id of the group you wish to retreive

    Returns:
        obj: Instance of Group
    """

    return Group.query.get(id)


def getFromName(name):
    """Retreive a group from the database given its name

    Args:
        name (str): The name of the group you wish to retreive

    Returns:
        obj: Instance of Group
    """

    return Group.query.filter_by(name=name).first()


def newMember(group_id, user_id):
    """Add a user with the given user_id to the group with the given group_id

    Args:
        group_id (int): The id of the group you wish to add a user to
        user_id (int): The id of the user you wish to add to a group
    """

    group = Group.query.get(group_id)
    user = User.query.get(user_id)
    group.members.append(user)
    sqlalchemy.session.commit()

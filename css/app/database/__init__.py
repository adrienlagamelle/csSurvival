from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from css.app import app

__all__ = ['user', 'comment', 'thread', 'group', 'subscription']

sqlalchemy = SQLAlchemy(app)
migrate = Migrate(app, sqlalchemy)

from . import user
from . import comment
from . import thread
from . import group
from . import subscription

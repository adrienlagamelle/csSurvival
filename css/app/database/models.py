'''Interface for the data stored in the database represented by
a collection of classees, called database models
The ORM layer within sqlalchemy do the translations required to map objects
created from these classes into rows in the proper tables
'''
from css.app import app, login
from . import sqlalchemy
import flask_whooshalchemy as whooshalchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


UserGroup = sqlalchemy.Table(
    'UserGroup',
    sqlalchemy.Column(
        'group_id',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('group.id'),
    ),
    sqlalchemy.Column(
        'user_id',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('user.id'),
    ),
)


class User(UserMixin, sqlalchemy.Model):
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True
    )
    username = sqlalchemy.Column(
        sqlalchemy.String(24),
        index=True,
        unique=True
    )
    email = sqlalchemy.Column(
        sqlalchemy.String(120),
        index=True,
        unique=True
    )
    password_hash = sqlalchemy.Column(
        sqlalchemy.String(128)
    )
    comments = sqlalchemy.relationship(
        'Comment',
        backref='author',
        lazy='dynamic'
    )
    threads = sqlalchemy.relationship(
        'Thread',
        backref='author',
        lazy='dynamic'
    )
    about = sqlalchemy.Column(
        sqlalchemy.String(140),
        index=True,
        unique=True
    )
    last_seen = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.utcnow
    )
    language = sqlalchemy.Column(
        sqlalchemy.String(2),
        default='en'
    )
    groups = sqlalchemy.relationship(
        'Group',
        secondary=UserGroup,
        backref=sqlalchemy.backref('members'),
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Thread(sqlalchemy.Model):
    __searchable__ = ['title', 'body']

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True
    )
    title = sqlalchemy.Column(
        sqlalchemy.String(140)
    )
    body = sqlalchemy.Column(
        sqlalchemy.String(140)
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('user.id')
    )
    group_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('group.id')
    )
    comments = sqlalchemy.relationship(
        'Comment',
        backref='parent',
        lazy='dynamic'
    )
    subscribers = sqlalchemy.relationship(
        'Subscription',
        backref='thread',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Thread {}>'.format(self.title)


class Comment(sqlalchemy.Model):
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True
    )
    body = sqlalchemy.Column(
        sqlalchemy.String(140)
    )
    timestamp = sqlalchemy.Column(
        sqlalchemy.DateTime,
        index=True,
        default=datetime.utcnow
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('user.id')
    )
    thread_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('thread.id')
    )

    def __repr__(self):
        return '<Comment {}>'.format(self.body)


class Subscription(sqlalchemy.Model):
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('user.id')
    )
    thread_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('thread.id')
    )
    email = sqlalchemy.Column(
        sqlalchemy.String(120)
    )
    username = sqlalchemy.Column(
        sqlalchemy.String(24),
        index=True,
    )

    def __repr__(self):
        return '<Subscription {}>'.format(self.user_id)


class Group(sqlalchemy.Model):
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True
    )
    name = sqlalchemy.Column(
        sqlalchemy.String(140)
    )
    threads = sqlalchemy.relationship(
        'Thread',
        backref='group',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Group {}>'.format(self.name)


whooshalchemy.whoosh_index(app, Thread)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

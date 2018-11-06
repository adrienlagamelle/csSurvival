"""Test for Full-Text Search functionality"""

import unittest
import os
from css.app import app
from css.app.database import sqlalchemy
from css.app.database import user
from css.app.database import thread
from css.app.database import comment


class UserProfile_TestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        sqlalchemy.create_all()

    def tearDown(self):
        sqlalchemy.drop_all()

    def test_search_nothing_found(self):
        a = thread.new('This is the title', 'This is the body', 1)
        b = thread.new('This is another title', 'This is another body', 2)

        c = thread.search('nothing')
        self.assertEqual(c, [])

    def test_search_onefound(self):
        a = thread.new('This is the title', 'This is the body', 1)
        b = thread.new('This is another title', 'This is another body', 2)

        c = str(thread.search('another'))
        self.assertEqual(c, '[<Thread This is another title>]')

    def test_search_title(self):
        a = thread.new('This is the title', 'This is the body', 1)
        b = thread.new('This is another title', 'This is another body', 2)

        c = str(thread.search('title'))
        self.assertEqual(c, '[<Thread This is the title>, <Thread This is another title>]')

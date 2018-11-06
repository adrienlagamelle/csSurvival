"""Test for database implementation"""

import unittest
from css.app import app
from css.app.database import sqlalchemy
from css.app.database import user
from css.app.database import thread
from css.app.database import comment


class Database_TestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        sqlalchemy.create_all()

    def tearDown(self):
        sqlalchemy.drop_all()

    def test_user(self):
        """ Test User """
        a = user.new('daniel', 'djp468@mun.ca', 'admin')
        b = user.get(1)
        c = user.getFromUsername('daniel')
        d = user.new('notDaniel', 'me@danielpower.ca', '1234')
        all = user.getAll()

        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertNotEqual(a, d)
        self.assertEqual(all[0], a)
        self.assertEqual(all[1], d)
        self.assertEqual(a.id, 1)
        self.assertEqual(d.id, 2)
        self.assertEqual(a.username, 'daniel')
        self.assertEqual(a.email, 'djp468@mun.ca')
        self.assertTrue(a.check_password('admin'))
        self.assertFalse(a.check_password('1234'))

    def test_thread(self):
        """ Test Thread """
        a = thread.new('This is the title', 'This is the body', 1)
        b = thread.new('This is another title', 'This is another body', 2)

        self.assertEqual(a.id, 1)
        self.assertEqual(b.id, 2)
        self.assertEqual(a.title, 'This is the title')
        self.assertEqual(b.title, 'This is another title')
        self.assertEqual(a.body, 'This is the body')
        self.assertEqual(b.body, 'This is another body')
        self.assertEqual(a.user_id, 1)
        self.assertEqual(b.user_id, 2)

    def test_comment(self):
        """ Test Comment """
        a = comment.new('This is a comment', 1, 1)
        b = comment.new('This is another comment', 1, 2)
        c = comment.new('This comment is by a different user', 2, 1)
        d = comment.new('This is another comment by a different user', 2, 1)

        self.assertEqual(a.body, 'This is a comment')
        self.assertEqual(b.body, 'This is another comment')
        self.assertEqual(c.body, 'This comment is by a different user')
        self.assertEqual(d.body, 'This is another comment by a different user')
        self.assertEqual(a.user_id, 1)
        self.assertEqual(b.user_id, 1)
        self.assertEqual(c.user_id, 2)
        self.assertEqual(d.user_id, 2)
        self.assertEqual(a.thread_id, 1)
        self.assertEqual(b.thread_id, 2)
        self.assertEqual(c.thread_id, 1)
        self.assertEqual(d.thread_id, 1)

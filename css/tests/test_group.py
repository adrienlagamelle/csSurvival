"""Test for Group module functionality"""
import unittest
import os
from css.app import app
from css.app.emailer import send_email
from css.app import database as db
from css.app.database import sqlalchemy
from css.app.database import user
from css.app.database import thread
from css.app.database import comment
from unittest import TestCase


class groupTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        sqlalchemy.create_all()
    
    def tearDown(self):
        sqlalchemy.session.remove()
        sqlalchemy.drop_all()

    """Test for register and login"""    
    def test_user(self):
        response = self.app.post(
            "/register",
               data = dict(
                username="username",
                email="username@example.com",
                password="123"
            )
        )
        self.assertEqual(response.status_code, 200)
        response = self.app.post(
            "/login",
            data = dict(
                username="username",
                password="123"
            )
        )
        self.assertEqual(response.status_code, 200)
    
    """Test for create group"""   
    def test_createGroup(self):
        response1 = self.app.post(
            "/register",
               data = dict(
                username="username",
                email="username@example.com",
                password="123",
            )
        )
        self.assertEqual(response1.status_code, 200)
        response2 = self.app.post(
            "/login",
            data = dict(
                username="username",
                password="123",
            )
        )
        self.assertEqual(response2.status_code, 200)
        response3 = self.app.post(
            "/createGroup",
            data = dict(
                name="groupname",
            )
        )
        self.assertEqual(response3.status_code, 302)
        
    """Test for add group member"""
    def test_addGroupMember(self):
        response1 = self.app.post(
            "/register",
               data = dict(
                username="username",
                email="username@example.com",
                password="123",
            )
        )
        self.assertEqual(response1.status_code, 200)
        response2 = self.app.post(
            "/login",
            data = dict(
                username="username",
                password="username@example.com",
            )
        )
        self.assertEqual(response2.status_code, 200)
        response3 = self.app.post(
            "/createGroup",
            data = dict(
                name="groupname",
            )
        )
        self.assertEqual(response3.status_code, 302)
        response4 = self.app.post(
            "/addGroupMember/1",
            data = dict(
                username="username",
            )
        )
        self.assertEqual(response4.status_code, 302)
   
    """Test for my group"""
    def test_myGroup(self):
        response1 = self.app.post(
            "/register",
               data = dict(
                username="username",
                email="username@example.com",
                password="123",
            )
        )
        self.assertEqual(response1.status_code, 200)
        response2 = self.app.post(
            "/login",
            data = dict(
                username="username",
                password="username@example.com",
            )
        )
        self.assertEqual(response2.status_code, 200)
        response3 = self.app.post(
            "/createGroup",
            data = dict(
                name="groupname",
            )
        )
        self.assertEqual(response3.status_code, 302)
        response4 = self.app.get(
            "/myGroups"
        )

        self.assertEqual(response4.status_code, 302)        

            
if __name__ == '__main__':
    unittest.main()



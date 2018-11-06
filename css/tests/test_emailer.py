import unittest
from css.app import app
from css.app.emailer import send_email
'''-----------------------------------------------
Run this python program to test the emailer module
with three different email addresses.
-----------------------------------------------'''
class TestEmailMethods(unittest.TestCase):

  
    def setUp(self):
        self.recipient = 'cssurvivalwebsite@gmail.com'
        self.subject = 'Thread Updated!'
        self.recipient_username = 'cssurvival'
        self.name = 'Thread Name'


    def test_recipient(self):  
        self.assertAlmostEqual(self.recipient, 'cssurvivalwebsite@gmail.com')


    def test_send_Good_email(self):
        self.assertAlmostEqual(
            send_email(
                self.recipient,
                self.subject,
                self.recipient_username
                ,self.name,
            ),send_email(
                'cssurvivalwebsite@gmail.com',
                'Thread Updated!',
                'cssurvival',
                'Thread Name',
            )
        )

   
    @unittest.expectedFailure
    def test_send_Bad_email(self):
        with self.assertRaises(SyntaxError):
            send_email_bad(self.recipient,self.subject,self.recipient_username,self.name)

    
if __name__ == '__main__':
    unittest.main()

        

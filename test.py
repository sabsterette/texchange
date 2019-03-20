# test.py

import unittest

from example import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()
        self.user.set_user_id('asy1433')
        self.user.set_user_name('amy14')
        self.user.set_email('asy27@case.edu')
        self.user.set_image_file('pixel.png')
    
    def test_user_creation(self):
        self.assertIsInstance(self.user, User)

    def test_user_id(self):
        expected_id = 'asy1433'
        self.assertEqual(expected_id, self.user.get_user_id)

    def test_user_name(self):
        expected_user_name = 'amy14'
        self.assertEqual(expected_user_name, self.user.get_user_name)

    def test_email(self):
        expected_email = 'asy27@case.edu'
        self.assertEqual(expected_email, self.user.get_email)
    
    def test_image_file(self):
        expected_image_file = 'pixel.png'
        self.assertEqual(expected_image_file, self.user.get_image_file)

    if __name__ == '__main__':
        unittest.main()
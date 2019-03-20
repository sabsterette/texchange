# test.py

import unittest

from faker import Faker

from example import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()
        self.user = User(
            id = self.fake.id(),
            user_name = self.fake.id(),
            email = self.fake.email(),
            image_file = self.fake.image_file()
        )
    
    def test_user_creation(self):
        self.assertIsInstance(self.user,User)

    def test_id(self):
        expected_id = self.user.id
        self.assertEqual(expected_id, self.user.id)

    def test_user_name(self):
        expected_user_name = self.user.user_name
        self.assertEqual(expected_user_name, self.user.user_name)

    def test_email(self):
        expected_email = self.user.email
        self.assertEqual(expected_email, self.user.email)
    
    def test_image_file(self):
        expected_image_file = self.user.image_file
        self.assertEqual(expected_image_file, self.user.image_file)
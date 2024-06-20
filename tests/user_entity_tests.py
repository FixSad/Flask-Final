import unittest
from app.models import User, Role

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        user = User()
        user.password = "test"
        self.assertTrue(user.password_hash is not None)

    def test_null_role(self):
        user = User()
        self.assertTrue(user.role == Role.Employee)

    def test_set_role(self):
        user = User()
        user.role = Role.Moderator
        self.assertTrue(user.role == Role.Moderator)

    def test_password_getter(self):
        user = User()
        user.password = "test"
        with self.assertRaises(AttributeError):
            password = user.password

    def test_password_verify(self):
        user = User()
        user.password = "test"
        self.assertTrue(user.password_verify("test"))
        self.assertFalse(user.password_verify("test2"))

    def test_salt(self):
        user = User()
        user.password = "test1"
        user2 = User()
        user2.password = "test2"
        self.assertTrue(user.password_hash != user2.password_hash)

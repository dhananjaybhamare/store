import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        """
        Unittest setup method to initialize app and database
        :return:
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Unittest teardown method to flush database
        :return:
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """
        Unittest to test if the application is created
        :return:
        """
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """
        Unittest to test of the application is running in testing mode
        :return:
        """
        self.assertTrue(current_app.config['TESTING'])
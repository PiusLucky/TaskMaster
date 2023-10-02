import os
import unittest
import json
from faker import Faker
from server import create_app, db

fake = Faker()
os.environ['FLASK_ENV'] = 'testing'


class AuthenticationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a Flask app with testing configuration
        cls.app = create_app("testing")
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Create the database tables for testing
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def register(self, full_name, email, password):

        # Convert the data dictionary to a JSON string
        data_json = json.dumps({
            "full_name": full_name,
            "email": email,
            "password": password
        })

        response = self.client.post(
            '/api/v1/user/users', data=data_json, content_type='application/json')

        return response

    def login(self, email, password):
        data_json = json.dumps({
            "email": email,
            "password": password
        })

        response = self.client.post(
            '/api/v1/user/users/login',  data=data_json, content_type='application/json')
        return response

    def test_register_endpoint(self):
        # Generate random data using Faker
        full_name = fake.name()
        email = fake.email()
        password = fake.password()

        # Register a new user with random data
        register_response = self.register(full_name, email, password)
        self.assertEqual(register_response.status_code, 200)
        self.assertEqual(register_response.content_type, "application/json")

    def test_login_endpoint(self):
        # Generate random data using Faker
        full_name = fake.name()
        email = fake.email()
        password = fake.password()

        self.register(full_name, email, password)

        login_response = self.login(email, password)
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.content_type, "application/json")


if __name__ == '__main__':
    unittest.main()

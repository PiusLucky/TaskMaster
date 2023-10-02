import os
import unittest
import json
import random
from faker import Faker
from server import create_app, db

fake = Faker()
os.environ['FLASK_ENV'] = 'testing'


class IntegrationTests(unittest.TestCase):
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

    def test_integration(self):
        full_name = fake.name()
        email = fake.email()
        password = fake.password()

        # Register a new user with random data
        user_register_response = self.client.post('/api/v1/user/users', data=json.dumps({
            "full_name": full_name,
            "email": email,
            "password": password
        }), content_type='application/json')

        self.assertEqual(user_register_response.status_code, 200)

        # Login with the registered user
        user_login_response = self.client.post('/api/v1/user/users/login', data=json.dumps({
            "email": email,
            "password": password
        }), content_type='application/json')

        access_token = user_login_response.json['data']['access_token']

        self.assertEqual(user_login_response.status_code, 200)

        # Proceed to create task
        task_data = {
            "title": fake.word(),
            "description": fake.paragraph(),
            "category": random.choice(["studies", "work", "other"]),
            "priority": random.choice(["high", "medium", "low"]),
            "dueDate": fake.date_between(start_date='today', end_date='+30d').strftime("%Y-%m-%d")
        }

        created_task_response = self.client.post('/api/v1/task/tasks', data=json.dumps(task_data), headers={
            "Authorization": f"Bearer {access_token}"
        }, content_type='application/json')

        self.assertEqual(created_task_response.status_code, 200)

        # Proceed to get all tasks
        get_tasks_response = self.client.get(
            f'/api/v1/task/tasks', headers={'Authorization': f'Bearer {access_token}'})

        self.assertEqual(get_tasks_response.status_code, 200)

        # Proceed to update task
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated Task Description",
        }
        task_id = created_task_response.json["data"]["id"]
        update_response = self.client.put(f'/api/v1/task/tasks/{task_id}', data=json.dumps(
            update_data), content_type='application/json', headers={'Authorization': f'Bearer {access_token}'})

        get_tasks_response = self.client.get(
            f'/api/v1/task/tasks', headers={'Authorization': f'Bearer {access_token}'})

        self.assertEqual(update_response.status_code, 200)

        # Proceed to delete tasks
        delete_response = self.client.delete(
            f'/api/v1/task/tasks/{task_id}', headers={'Authorization': f'Bearer {access_token}'})

        self.assertEqual(delete_response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

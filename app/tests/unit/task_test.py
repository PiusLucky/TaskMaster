import os
import unittest
import json
import random
from faker import Faker
from server import create_app, db

fake = Faker()
os.environ['FLASK_ENV'] = 'testing'


class TestTaskAPI(unittest.TestCase):
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

    def register_user(self):
        # Generate random data using Faker
        full_name = fake.name()
        email = fake.email()
        password = fake.password()

        # Register a new user with random data
        self.client.post('/api/v1/user/users', data=json.dumps({
            "full_name": full_name,
            "email": email,
            "password": password
        }), content_type='application/json')
        return email, password

    def login_user(self, email, password):
        # Login with the registered user
        response = self.client.post('/api/v1/user/users/login', data=json.dumps({
            "email": email,
            "password": password
        }), content_type='application/json')

        return response.json['data']['access_token']

    def create_task(self, access_token):
        # Create a task with random data
        task_data = {
            "title": fake.word(),
            "description": fake.paragraph(),
            "category": random.choice(["studies", "work", "other"]),
            "priority": random.choice(["high", "medium", "low"]),
            "dueDate": fake.date_between(start_date='today', end_date='+30d').strftime("%Y-%m-%d")
        }

        response = self.client.post('/api/v1/task/tasks', data=json.dumps(task_data), headers={
            "Authorization": f"Bearer {access_token}"
        }, content_type='application/json')

        return response

    def test_create_task_endpoint(self):
        # Register a new user
        email, password = self.register_user()

        # Login with the registered user
        access_token = self.login_user(email, password)

        # Create a task with the access token
        response = self.create_task(access_token)
        responseData = response.json["data"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertIn("id", responseData)
        self.assertIn("user_id", responseData)
        self.assertIn("title", responseData)

    def test_get_task_endpoint(self):
        # Register a new user
        email, password = self.register_user()
        # Create a task
        access_token = self.login_user(email, password)
        create_response = self.create_task(access_token)

        # Extract the task_id from the create_response JSON
        task_id = create_response.json["data"]["id"]

        # Send a GET request to retrieve the task
        get_tasks_response = self.client.get(
            f'/api/v1/task/tasks', headers={'Authorization': f'Bearer {access_token}'})

        taskIdInDB = get_tasks_response.json["data"]["tasks"][0]["id"]

        self.assertEqual(get_tasks_response.status_code, 200)
        self.assertEqual(get_tasks_response.content_type, "application/json")
        # We have to make sure the created task above is in the tasks list
        self.assertEqual(task_id, taskIdInDB)
        # Check for pagination
        self.assertEqual(
            get_tasks_response.json["data"]["pagination"]["page"], 1)
        self.assertEqual(
            get_tasks_response.json["data"]["pagination"]["total_elements"], 1)
        self.assertEqual(
            get_tasks_response.json["data"]["pagination"]["limit"], 10)

    def test_update_task_endpoint(self):
        # Register a new user
        email, password = self.register_user()
        # Create a task
        access_token = self.login_user(email, password)
        create_response = self.create_task(access_token)

        task_id = create_response.json["data"]["id"]

        update_data = {
            "title": "Updated Task Title",
            "description": "Updated Task Description",
        }

        update_response = self.client.put(f'/api/v1/task/tasks/{task_id}', data=json.dumps(
            update_data), content_type='application/json', headers={'Authorization': f'Bearer {access_token}'})
        updated_json_response = update_response.json["data"]

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.content_type, "application/json")
        self.assertEqual(updated_json_response["title"], update_data["title"])
        self.assertEqual(
            updated_json_response["description"], update_data["description"])

    def test_delete_task_endpoint(self):
        # Register a new user
        email, password = self.register_user()
        # Create a task
        access_token = self.login_user(email, password)
        create_response = self.create_task(access_token)

        # Extract the task_id from the create_response JSON
        task_id = create_response.json["data"]["id"]

        # Send a DELETE request to delete the task
        delete_response = self.client.delete(
            f'/api/v1/task/tasks/{task_id}', headers={'Authorization': f'Bearer {access_token}'})

        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.content_type, "application/json")

        # After deletion, the task shouldn't exist anymore
        get_tasks_response = self.client.get(
            f'/api/v1/task/tasks', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(
            len(get_tasks_response.json["data"]["tasks"]), 0)
        self.assertEqual(
            get_tasks_response.json["data"]["pagination"]["total_pages"], 0)
        self.assertEqual(
            get_tasks_response.json["data"]["pagination"]["total_elements"], 0)


if __name__ == '__main__':
    unittest.main()

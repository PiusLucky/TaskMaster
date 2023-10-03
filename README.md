<p align="center">
  <img src="https://github.com/PiusLucky/TaskMaster-FE/raw/main/public/images/logo.png" alt="TaskMaster Logo" width="100">
</p>

# TaskMaster Backend

TaskMaster Backend is the server component of the TaskMaster project, responsible for managing tasks, user authentication, and data storage.

## Deployed version
`Backend Server`: https://taskmaster-yk6i.onrender.com/


## Project Setup

1. Clone the repository:

```bash
    git clone https://github.com/yourusername/taskmaster-backend.git
    cd taskmaster-backend
```

2. Setup virtual environment & Install dependencies:

```bash
  python -m venv .venv
  .\venv\Scripts\activate
```

```bash
   pip install -r requirements.txt
```



➡️ Database setup

```bash
   flask db init
   flask db migrate
   flask db upgrade
```

🌐 Run Tests (Both Unit and integration tests)

```bash
    python -m pytest
```

![image](https://github.com/PiusLucky/TaskMaster/assets/32282934/53a34e3a-f779-475e-8aed-97306843da45)


3. Set up your environment variables by creating a `.env` file based on the provided `env.sample` file.

## Environment Variables

Make sure to set the following environment variables in your `.env` file:

- `FLASK_APP`: Set to `server`
- `FLASK_ENV`: Set to `development` or `production` depending on your environment.
- `DATABASE_URI`: Your local or staging PostgreSQL database URI.
- `SECRET_KEY`: Any strong secret key for application security.
- `JWT_SECRET_KEY`: Any strong secret key for JSON Web Tokens (JWT).

4. Run the Flask application

   ```bash
   flask run
   ```

The backend should now be running on `http://localhost:5000`.



## Features

- Create tasks with titles, descriptions, categories, priorities, and due dates.
- Update and edit existing tasks.
- Delete tasks when they are no longer needed.
- Categorize tasks based on their purpose or category.
- Set priorities to keep track of important tasks.
- User authentication and authorization with JWT.
- Token revocation and security measures.
- Comprehensive task management.

Feel free to explore the backend and integrate it with the frontend to use TaskMaster's full functionality!

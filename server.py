import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask import request, Response
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
csrf = CSRFProtect()


def create_app(environment="development"):
    app = Flask(__name__)

    print(environment)

    databaseUri = None

    # Assume we only have two environments
    if environment == "development":
        databaseUri = os.getenv("DATABASE_URI")
    elif environment != "development":
        # Fake Test DB URL
        databaseUri = "postgresql://postgres:xxxxxxxxx@localhost:5432/taskTrackerTest"

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            res = Response()
            res.headers['X-Content-Type-Options'] = '*'
            return res

    CORS().init_app(app)

    if environment == "testing":
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = databaseUri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Replace with a strong secret key
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    # Disable CSRF protection, since we are going RESTful
    app.config['WTF_CSRF_ENABLED'] = False
    # Replace with a strong secret key
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        hours=1)  # Token expiration time

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()

    # Register API routes
    from app.routes import task_route, health_check_route, user_route
    app.register_blueprint(health_check_route.health_check_route)
    app.register_blueprint(user_route.user_route)
    app.register_blueprint(task_route.task_route)

    return app


if __name__ == '__main__':
    app = create_app("development")
    app.run(debug=True)

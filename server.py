from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Lucky&Pius&5@localhost:5432/taskTracker"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'ZVuPI/FBIoHi|1$'  # Replace with a strong secret key
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection
    app.config["JWT_SECRET_KEY"] = "EO=E@NLD4-t)c!Y"  # Replace with a strong secret key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Token expiration time

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    jwt = JWTManager(app)
    
    CORS(app, supports_credentials=True)

    with app.app_context():
        db.create_all()

    # Register API routes
    from app.routes import task_route, health_check_route, user_route
    app.register_blueprint(health_check_route.health_check_route)
    app.register_blueprint(user_route.user_route)
    app.register_blueprint(task_route.task_route)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

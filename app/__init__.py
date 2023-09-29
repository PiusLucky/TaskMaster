from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import task_tracker_route

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgress:password@localhost/taskTracker"

db = SQLAlchemy(app)

# Register API route
app.register_blueprint(task_tracker_route.item_routes)

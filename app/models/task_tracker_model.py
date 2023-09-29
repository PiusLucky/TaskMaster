from app import db

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    dueDate = db.Column(db.Date, nullable=True)  # Add the dueDate field

    def __init__(self, title, description=None, dueDate=None):
        self.title = title
        self.description = description
        self.dueDate = dueDate  # Initialize the dueDate field
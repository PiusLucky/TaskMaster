from app.models import BaseTable
from sqlalchemy import Column, String, ForeignKey, Date, Text, UUID


class TaskModel(BaseTable):
    __tablename__ = 'taskTable'

    user_id = Column(UUID(),  ForeignKey('userTable.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    dueDate = Column(Date, nullable=False)

    def __init__(self, user_id, title, description, category, priority, dueDate):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.dueDate = dueDate

    def as_dict(self):
        # Convert the object's attributes to a dictionary
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'dueDate': self.dueDate,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

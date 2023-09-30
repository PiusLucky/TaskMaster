from app.models import BaseTable
from sqlalchemy import Column, String, ForeignKey, Date, Text, UUID

class TaskModel(BaseTable):
    __tablename__ = 'taskTable'

    user_id = Column(UUID(),  ForeignKey('userTable.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(255), nullable=False)
    dueDate = Column(Date, nullable=False)  

    def __init__(self, user_id, title, description, priority, dueDate):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.priority = priority
        self.dueDate = dueDate  
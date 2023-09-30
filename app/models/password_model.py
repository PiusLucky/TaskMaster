from app.models import BaseTable
from sqlalchemy import Column, String, ForeignKey, UUID

class PasswordModel(BaseTable):
    __tablename__ = 'passwordTable'

    user_id = Column(UUID(),  ForeignKey('userTable.id'))
    password = Column(String(255), nullable=False)

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password 

    def as_dict(self):
        # Convert the object's attributes to a dictionary
        return {
            'password': self.password,
        }
from app.models import BaseTable
from sqlalchemy import Column, String

class UserModel(BaseTable):
    __tablename__ = 'userTable'

    full_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)

    def __init__(self, full_name, email):
        self.full_name = full_name
        self.email = email 

        
    def as_dict(self):
        # Convert the object's attributes to a dictionary
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
        }
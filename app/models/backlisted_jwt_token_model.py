
from app.models import BaseTable
from sqlalchemy import Column, String


class BlacklistedTokenModel(BaseTable):
    __tablename__ = 'blacklistedTokenTable'

    jti = Column(String(36), unique=True, nullable=False)

    def __init__(self, jti):
        self.jti = jti
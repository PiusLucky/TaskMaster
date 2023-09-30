from server import db
import uuid

def get_uuid():
    return uuid.uuid4().hex

class BaseTable(db.Model):
    __abstract__ = True
    id = db.Column(db.UUID(), primary_key=True, default=get_uuid)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
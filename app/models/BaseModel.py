from sqlalchemy import text

from app import db
from sqlalchemy.sql import func


class BaseModel:
    CREATED_AT = db.Column(db.TIMESTAMP, default=func.now())
    UPDATED_AT = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()

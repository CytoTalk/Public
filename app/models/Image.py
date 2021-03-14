from app import db
from sqlalchemy.sql import func


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    path = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    description = db.Column(db.Text)
    CREATED_AT = db.Column(db.TIMESTAMP, default=func.now())
    UPDATED_AT = db.Column(db.TIMESTAMP, default=func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()

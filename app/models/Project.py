from app import db
from sqlalchemy.sql import func


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.Text)
    CREATED_AT = db.Column(db.TIMESTAMP, default=func.now())
    UPDATED_AT = db.Column(db.TIMESTAMP, default=func.now())
    categories = db.relationship('Category', backref='project', lazy=True)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()

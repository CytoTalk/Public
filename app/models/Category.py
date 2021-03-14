from app import db
from sqlalchemy.sql import func


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    description = db.Column(db.Text)
    CREATED_AT = db.Column(db.TIMESTAMP, default=func.now())
    UPDATED_AT = db.Column(db.TIMESTAMP, default=func.now())
    images = db.relationship('Image', backref='category', lazy=True)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()

from app import db

from app.models.BaseModel import BaseModel


class Category(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(1000))
    images = db.relationship('Image', backref='category', lazy=True)

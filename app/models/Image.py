from app import db

from app.models.BaseModel import BaseModel


class Image(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    path = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    description = db.Column(db.Text)

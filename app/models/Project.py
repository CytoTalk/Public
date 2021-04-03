from app import db
from app.models.BaseModel import BaseModel


class Project(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.Text)
    categories = db.relationship('Category', backref='project', lazy=True, cascade="all,delete")
    type = db.Column(db.String(15), default="single")

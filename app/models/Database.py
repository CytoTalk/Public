from app import db

from app.models.BaseModel import BaseModel


class Database(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.Text)
    categories = db.relationship('DatabaseCategory', backref='database', lazy=True, cascade="all,delete")


class DatabaseCategory(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    database_id = db.Column(db.Integer, db.ForeignKey('database.id'))
    description = db.Column(db.Text)
    images = db.relationship('Image', backref='subproject', lazy=True, cascade="all,delete")


class Image(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    path = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('database_category.id'))
    description = db.Column(db.Text)

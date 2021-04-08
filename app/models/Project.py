from app import db
from app.models.BaseModel import BaseModel


class Project(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.Text)
    subprojects = db.relationship('SubProject', backref='project', lazy=True, cascade="all,delete")


class SubProject(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(1000))
    type = db.Column(db.String(1000))
    columns = db.relationship('ExcelColumn', backref='subproject', lazy=True, cascade="all,delete")
    images = db.relationship('ImageCategory', backref='subproject', lazy=True, cascade="all,delete")


class ImageCategory(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    sub_project_id = db.Column(db.Integer, db.ForeignKey('subproject.id'))
    description = db.Column(db.Text)
    images = db.relationship('ImageStore', backref='category', lazy=True, cascade="all,delete")


class ImageStore(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    path = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('imagecategory.id'))
    description = db.Column(db.Text)
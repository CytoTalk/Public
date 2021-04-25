from app import db
from app.models.BaseModel import BaseModel

allowed_user = db.Table(
    'allowed',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)


class Project(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.Text)
    allowed = db.relationship("User", secondary=allowed_user)
    # ''' Add private/public check'''
    status = db.Column("private", db.Boolean(), default=True, nullable=True)

    subprojects = db.relationship('SubProject', backref='project', lazy=True, cascade="all,delete")


class SubProject(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(1000))
    type = db.Column(db.String(1000))
    columns = db.relationship('ExcelColumn', backref='subproject', lazy=True, cascade="all,delete", order_by="asc("
                                                                                                             "ExcelColumn.id)", )
    categories = db.relationship('ImageCategory', backref='subproject', lazy=True, cascade="all,delete")


class ImageCategory(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    subproject_id = db.Column(db.Integer, db.ForeignKey('sub_project.id'))
    description = db.Column(db.Text)
    images = db.relationship('ImageStore', backref='category', lazy=True, cascade="all,delete")


class ImageStore(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    path = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('image_category.id'))
    description = db.Column(db.Text)

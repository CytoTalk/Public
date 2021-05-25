from flask_login import current_user

from app import db
from app.models.BaseModel import BaseModel


class AllowedUser(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))


class Project(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.Text)
    # ''' Add private/public check'''
    is_public = db.Column(db.Boolean(), default=True, nullable=True)

    subprojects = db.relationship('SubProject', backref='project', lazy=True, cascade="all,delete")
    allowed_users = db.relationship("AllowedUser", backref="project", lazy=True, cascade="all,delete")

    def user_has_permission(self) -> bool:
        return current_user.is_authenticated and current_user in self.allowed_users and not self.is_public


class SubProject(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(1000))
    type = db.Column(db.String(1000))
    columns = db.relationship('ExcelColumn',
                              backref='subproject',
                              lazy=True,
                              cascade="all,delete",
                              order_by="asc(ExcelColumn.id)",)

    features = db.relationship('Feature',
                               backref='subproject',
                               lazy=True,
                               cascade="all,delete",
                               order_by="asc(Feature.id)",)

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

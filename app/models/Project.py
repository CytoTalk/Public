from typing import List

from flask_login import current_user
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import backref

from app import db
from app.models.BaseModel import BaseModel


class AllowedUser(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    model_id = db.Column(db.Integer, index=True)
    permissions = db.Column(ARRAY(db.Unicode))
    model = db.Column(db.String, )


def allowed_projects_for_user() -> List:
    if current_user.is_authenticated:
        return Project.query.filter(or_(Project.is_public, Project.allowed_users.any(user_id=current_user.id)))
    return Project.query.filter(Project.is_public)


class Project(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.Text)
    # ''' Add private/public check'''
    is_public = db.Column(db.Boolean(), default=True, nullable=True)

    subprojects = db.relationship('SubProject', backref='project', lazy=True, cascade="all,delete")
    allowed_users = db.relationship("AllowedUser",
                                    backref=backref("project",
                                                    passive_deletes=True),
                                    cascade_backrefs=False,
                                    lazy="joined",
                                    cascade="all",
                                    single_parent=True,
                                    foreign_keys=[id],
                                    uselist=True,
                                    primaryjoin='Project.id==AllowedUser.model_id and '
                                                '\'Project\' == AllowedUser.model '
                                    )

    def user_has_permission(self) -> bool:
        if self.is_public:
            return True
        if current_user.is_authenticated:
            return current_user.has_permission(self)
        return False


class SubProject(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    description = db.Column(db.Text)
    file_path = db.Column(db.String(1000))
    is_public = db.Column(db.Boolean(), default=True, nullable=True)
    type = db.Column(db.String(1000))
    columns = db.relationship('ExcelColumn',
                              backref='subproject',
                              lazy=True,
                              cascade="all,delete",
                              order_by="asc(ExcelColumn.id)", )

    features = db.relationship('Feature',
                               backref='subproject',
                               lazy=True,
                               cascade="all,delete",
                               order_by="asc(Feature.id)", )

    categories = db.relationship('ImageCategory', backref='subproject', lazy=True, cascade="all,delete")

    allowed_users = db.relationship("AllowedUser",
                                    backref=backref("subproject", passive_deletes=True),
                                    cascade_backrefs=False,
                                    lazy="joined",
                                    cascade="all",
                                    foreign_keys=[id],
                                    uselist=True,
                                    primaryjoin='SubProject.id==AllowedUser.model_id and '
                                                '\'SubProject\' == AllowedUser.model '
                                    )

    def user_has_permission(self) -> bool:
        if self.is_public:
            return True
        if current_user.is_authenticated:
            return current_user.has_permission(self)
        return False


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

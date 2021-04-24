from flask_authorize import RestrictionsMixin, AllowancesMixin, PermissionsMixin
from flask_login import UserMixin

from app import db
from app.models.BaseModel import BaseModel

userAllowed = db.Table(
    "user_group", db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id"))
)

user_role = db.Table(
    'user_role', db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class User(UserMixin, db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    email_verified_at = db.Column(db.TIMESTAMP)

    '''priviledges'''
    roles = db.relationship('Role', secondary=user_role)
    groups = db.relationship('Group', secondary=userAllowed)


class Group(db.Model, RestrictionsMixin):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Role(db.Model, AllowancesMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Project(db.Model, BaseModel, PermissionsMixin):
    __permissions__ = dict(
        owner=['read', 'update', 'delete', 'revoke'],
        group=['read'],
        other=['read']
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.Text)

    # ''' Add private/public check'''
    # status = db.Column("private", db.Boolean(), default=True, nullable=True)

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

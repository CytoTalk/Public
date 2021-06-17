from flask_login import UserMixin
from sqlalchemy.orm import backref

from app import db
from app.models.BaseModel import BaseModel
from app.models.Project import AllowedUser


class User(UserMixin, db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    email_verified_at = db.Column(db.TIMESTAMP)
    project_permissions = db.relationship("AllowedUser", backref=backref("user"), uselist=True, lazy="dynamic",
                                          cascade="all,delete")

    def has_permission(self, model):
        return self.project_permissions.filter(
            AllowedUser.model == model.__class__.__name__,
            AllowedUser.model_id == model.id).first()

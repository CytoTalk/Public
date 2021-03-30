from app import db
from app.models.BaseModel import BaseModel


class Entity(db.Model, BaseModel):
    __tablename__ = 'entities'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.Text)
    fields = db.relationship('EntityField', backref='entity', lazy=True)


class EntityField(db.Model, BaseModel):
    __tablename__ = 'entity_fields'
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    title = db.Column(db.String(1000))
    description = db.Column(db.Text)
    records = db.relationship('EntityRecord', backref='field', lazy=True)


class EntityRecord(db.Model, BaseModel):
    __tablename__ = 'entity_records'
    id = db.Column(db.Integer, primary_key=True)
    entity_field_id = db.Column(db.Integer, db.ForeignKey('entity_fields.id'))
    value = db.Column(db.Text)
    batch_id = db.Column(db.String(200))

from app import db
from app.models.BaseModel import BaseModel


class Service(db.Model, BaseModel):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    short_description = db.Column(db.String(300))
    long_description = db.Column(db.TEXT)
    slug = db.Column(db.String, index=True, unique=True)
    price = db.Column(db.Integer)
    main_picture = db.Column(db.String)
    images = db.relationship('ServiceImage', backref='service', lazy=True, cascade='all,delete')


class ServiceImage(db.Model, BaseModel):
    __tablename__ = 'services_images'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String)
    url = db.Column(db.String)
    is_main_picture = db.Column(db.Boolean, default=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

from app import db
from app.models.BaseModel import BaseModel


class Course(db.Model, BaseModel):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    short_description = db.Column(db.String(300))
    long_description = db.Column(db.TEXT)
    slug = db.Column(db.String, index=True, unique=True)
    price = db.Column(db.Integer)
    main_picture = db.Column(db.String)
    images = db.relationship('CourseImage', backref='course', lazy=True, cascade='all,delete')


class CourseImage(db.Model, BaseModel):
    __tablename__ = 'courses_images'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String)
    url = db.Column(db.String)
    is_main_picture = db.Column(db.Boolean, default=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))



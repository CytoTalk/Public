from app import db
from app.models.BaseModel import BaseModel


class MonthlyPlan(db.Model, BaseModel):
    __tablename__ = 'monthly_plans'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    short_description = db.Column(db.String(300))
    long_description = db.Column(db.TEXT)
    slug = db.Column(db.String, index=True, unique=True)
    price = db.Column(db.Integer)
    main_picture = db.Column(db.String)
    images = db.relationship('MonthlyPlanImage', backref='monthly_plan', lazy=True, cascade='all,delete')


class MonthlyPlanImage(db.Model, BaseModel):
    __tablename__ = 'monthly_plans_images'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String)
    url = db.Column(db.String)
    is_main_picture = db.Column(db.Boolean, default=False)
    monthly_plan_id = db.Column(db.Integer, db.ForeignKey('monthly_plans.id'))

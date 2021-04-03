from app import db
from app.models.BaseModel import BaseModel


class ExcelColumn(db.Model, BaseModel):
    __tablename__ = 'excel_columns'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    title = db.Column(db.String(1000))
    description = db.Column(db.Text)
    records = db.relationship('ExcelRecord', backref='field', lazy=True, cascade="all,delete")


class ExcelRecord(db.Model, BaseModel):
    __tablename__ = 'excel_records'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    column_id = db.Column(db.Integer, db.ForeignKey('excel_columns.id'))
    value = db.Column(db.Text)
    batch_id = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.value,
            'text': self.value
        }

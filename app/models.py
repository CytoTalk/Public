from . import db


class Project(db.Model):
    __tablename__ = 'database'
    id = db.Column(db.Integer,primary_key=True)
    project_name = db.Column(db.String(255),nullable=False)
    project_category = db.relationship('Category', backref='database', lazy='dynamic')

    def __repr__(self):
        return f'Project {self.project_name}'


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    category_name = db.Column(db.String(255),nullable=False)
    project_id = db.Column(db.Integer,db.ForeignKey("database.id"))
    images = db.relationship('Image', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'Category {self.category_name}'
    

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer,primary_key=True)
    image_path = db.Column(db.String())
    category_id = db.Column(db.Integer,db.ForeignKey("category.id"))

    def __repr__(self):
        return f'Project {self.image_path}'


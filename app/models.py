from . import db
# from . import db, login_manager
# from werkzeug.security import generate_password_hash,check_password_hash
# from flask_login import UserMixin
# from datetime import datetime
# from . import login_manager

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    image = db.Column(db.String(),nullable=False)
    category = db.Column(db.String(255),nullable=False)
    description = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_post(id):
        post = Blog.query.filter_by(id=id).first()

        return post
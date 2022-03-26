
from datetime import datetime
from artistry import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.png')
    password = db.Column(db.String(60), nullable=False)

    # relations
    posts = db.relationship('Post', backref='author', lazy=True)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'User("{self.name}", "{self.username}", "{self.email}", "{self.image_file}")'

"""
The Post models
"""
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    photo_file = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    date_posted = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def __repr__(self):
        return f'Post("{self.title}", "{self.type}", "{self.photo_file}")'


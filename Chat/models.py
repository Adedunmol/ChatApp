from . import db
from . import login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    profile_picture = db.Column(db.String())
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'<id:{self.id}, username:{self.username}, email:{self.email}, profile_picture: {self.profile_picture}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(), nullable=False)
    picture = db.Column(db.String(), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<username:{self.caption}, email:{self.picture}, post_owner: {self.user_id}>'

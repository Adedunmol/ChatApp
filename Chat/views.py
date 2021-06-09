from flask import Blueprint, render_template
from .models import Post, User
from . import db


views = Blueprint('views', __name__)


@views.route('/')
def home():
    post = Post.query.all()
    users = User.query.all()
    return render_template('home.html', posts=post)


@views.route('/about')
def about():
    return 'hello'

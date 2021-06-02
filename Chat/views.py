from flask import Blueprint, render_template
from .models import Post
from . import db


views = Blueprint('views', __name__)


@views.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@views.route('/about')
def about():
    return 'hello'

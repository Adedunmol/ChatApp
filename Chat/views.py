from flask import Blueprint, render_template


views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('post.html')


@views.route('/about')
def about():
    return 'hello'

from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from . import bcrypt, db, socketio
from .models import User, Post
from flask_login import login_user, logout_user, login_required, current_user
from PIL import Image
from secrets import token_hex
import os
from flask_socketio import send, join_room, leave_room
from time import localtime, strftime

auth = Blueprint('auth', __name__)

ROOMS = ['Fashion', 'Music', 'Games', 'Coding']


def save_image(img):
    picture_name = token_hex(8)
    _, picture_ext = os.path.splitext(img.filename)
    picture_fn = picture_name + '.jpg'
    picture_path = os.path.join(auth.root_path, 'static/image', picture_fn)

    size = (125, 125)
    i = Image.open(img)
    i.thumbnail(size)
    jpg_img = i.convert('RGB')
    jpg_img.save(picture_path, quality=95)

    return picture_fn


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_name = save_image(form.image.data)
        else:
            flash('Please upload a picture', category='danger')
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_pw = bcrypt.generate_password_hash(password, 14).decode('utf-8')
        try:
            user = User(username=username, email=email, password=hashed_pw, profile_picture=picture_name)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created', category='success')
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
        finally:
            db.session.close()
    return render_template('Registration.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You are now logged in', category='success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash('The details you entered are not correct', category='danger')
    return render_template('Login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_name = save_image(form.image.data)
            current_user.profile_picture = picture_name
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
    form.email.data = current_user.email
    form.username.data = current_user.username
    image = url_for('static', filename='image/' + current_user.profile_picture)
    return render_template('account.html', form=form, image=image)


@auth.route('/new-post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        picture_name = save_image(form.image.data)
        caption = form.caption.data
        try:
            post = Post(caption=caption, picture=picture_name, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been posted.', category='success')
            return redirect(url_for('views.home'))
        except:
            db.session.rollback()
        finally:
            db.session.close()
    return render_template('new_post.html', form=form)


@auth.route('/users/<int:user_id>')
def users(user_id):
    return 'hello'


@auth.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html', username=current_user.username, room=ROOMS)


@socketio.on('message')
def message(data):

    print(f'\n\n{data}\n\n')
    send({'msg': data['msg'], 'username': data['username'],
          'time_stamp': strftime('%b-%d %I:%M%p', localtime()), 'room': data['room']})


@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg': data['username'] + "has joined the " + data['room']}, room=data['room'])


@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg': data['username'] + "has left the " + data['room']}, room=data['room'])

from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from . import bcrypt, db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from PIL import Image
from secrets import token_hex
import os

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_pw = bcrypt.generate_password_hash(password, 14).decode('utf-8')
        try:
            user = User(username=username, email=email, password=hashed_pw)
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


def save_image(img):
    picture_name = token_hex(16)
    _, picture_ext = os.path.splitext(img.filename)
    picture_fn = picture_name + picture_ext
    picture_path = os.path.join(auth.root_path, 'static/', picture_fn)

    size = (150, 150)
    i = Image.open(img)
    i.thumbnail(size)
    i.save(picture_path)

    return picture_fn


@auth.route('/account')
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
    return render_template('account.html', form=form)

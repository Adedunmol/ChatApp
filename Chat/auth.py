from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import RegistrationForm, LoginForm
from . import bcrypt, db
from .models import User
from flask_login import login_user, logout_user, login_required

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
            login_user(user,)
            return redirect(url_for('views.home'))
    return render_template('Login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))

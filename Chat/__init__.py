from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '816618bb8c542b409588c5b23b64b9f7'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dunmola@localhost:5432/chat'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False

    from .models import User

    from .auth import auth
    from .views import views

    app.register_blueprint(auth)
    app.register_blueprint(views)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app

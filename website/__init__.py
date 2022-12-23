from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from os import path

db = SQLAlchemy()
DB_NAME = "Chatterz.db"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///static/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "Aladdin's most awaited site"
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth,  url_prefix='/')

    from .models import User, Messages

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.refresh_view = 'auth.relogin'
    login_manager.needs_refresh_message = (u"Session timed out, please re-login")
    login_manager.needs_refresh_message_category = "info"
    login_manager.init_app(app)

    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app

def create_database(app):
    if not path.exists('website/static/'+DB_NAME):
        db.create_all(app=app)
        print("Database Created Successfully")
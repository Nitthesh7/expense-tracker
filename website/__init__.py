import os
from os import path
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

load_dotenv()

secret_key = os.environ.get('SECRET_KEY')
db_name = os.environ.get('DB_NAME')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    # all routes can be accessed from root url
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Entry

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # loading user id from database for sessions (current_user)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    # creating the database only once
    if not path.exists('instance/' + db_name):
        with app.app_context(): 
            db.create_all()
        print('Database Created!!')
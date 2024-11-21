from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,template_folder = 'templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./testdb.db"  # Fix the URI format here
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = 'SOME KEY'
    
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    bcrypt = Bcrypt(app)

    from routes import register_routes
    register_routes(app,db,bcrypt)

    migrate = Migrate(app,db)

    # from import_data import import_csv_to_db
    # import_csv_to_db(app,db)

    return app

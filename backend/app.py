from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()


def create_app():
    app = Flask(__name__,template_folder = 'templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./testdb.db"  # Fix the URI format here
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from routes import register_albums,register_users,register_lists
    register_albums(app,db)
    register_users(app,db)
    register_lists(app,db)

    migrate = Migrate(app,db)

    return app

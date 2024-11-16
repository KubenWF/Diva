from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

db = SQLAlchemy()


def create_app():
    app = Flask(__name__,template_folder = 'templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./testdb.db"  # Fix the URI format here
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from routes.user_route import register_users
    register_users(app,db)

    migrate = Migrate(app,db)

    return app
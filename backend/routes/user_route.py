from flask import render_template,request
from models import User

def register_users(app,db):
    
    @app.route('/')
    def index():
        users = User.query.all()
        return str(users)
